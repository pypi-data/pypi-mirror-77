import collections
import random
import uuid
from copy import deepcopy
from datetime import timedelta
from typing import Text, List
from warnings import warn

from ctpbee.constant import OrderRequest, Offset, Direction, OrderType, OrderData, CancelRequest, TradeData, BarData, \
    TickData, PositionData, Status, Exchange
from ctpbee.exceptions import ConfigError
from ctpbee.func import helper
from ctpbee.looper.account import Account


class Action:
    def __init__(self, looper):
        """ 将action这边报单 """
        self.looper = looper

    def buy(self, price, volume, origin, price_type: OrderType = OrderType.LIMIT, **kwargs):
        if not isinstance(self.looper.params['slippage_buy'], float) and not isinstance(
                self.looper.params['slippage_buy'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        req = OrderRequest(price=price, volume=volume, exchange=origin.exchange, offset=Offset.OPEN,
                           direction=Direction.LONG, type=price_type, symbol=origin.symbol)
        return self.looper.send_order(req)

    def short(self, price, volume, origin, price_type: OrderType = OrderType.LIMIT, **kwargs):
        if not isinstance(self.looper.params['slippage_short'], float) and not isinstance(
                self.looper.params['slippage_short'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        req = OrderRequest(price=price, volume=volume, exchange=origin.exchange, offset=Offset.OPEN,
                           direction=Direction.SHORT, type=price_type, symbol=origin.symbol)
        return self.looper.send_order(req)

    @property
    def position_manager(self):
        return self.looper.account.position_manager

    def sell(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData] = None,
             price_type: OrderType = OrderType.LIMIT, stop: bool = False, lock: bool = False, **kwargs):

        if not isinstance(self.looper.params['slippage_sell'], float) and not isinstance(
                self.looper.params['slippage_sell'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        price = price + self.looper.params['slippage_sell']
        req_list = [helper.generate_order_req_by_var(volume=x[1], price=price, offset=x[0], direction=Direction.LONG,
                                                     type=price_type, exchange=origin.exchange,
                                                     symbol=origin.symbol) for x in
                    self.get_req(origin.local_symbol, Direction.SHORT, volume, self.looper)]
        return [self.looper.send_order(req) for req in req_list if req.volume != 0]

    def cover(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData],
              price_type: OrderType = OrderType.LIMIT, stop: bool = False, lock: bool = False, **kwargs):
        if not isinstance(self.looper.params['slippage_cover'], float) and not isinstance(
                self.looper.params['slippage_cover'], int):
            raise ConfigError(message="滑点配置应为浮点小数")
        price = price + self.looper.params['slippage_cover']
        req_list = [helper.generate_order_req_by_var(volume=x[1], price=price, offset=x[0], direction=Direction.SHORT,
                                                     type=price_type, exchange=origin.exchange,
                                                     symbol=origin.symbol) for x in
                    self.get_req(origin.local_symbol, Direction.LONG, volume, self.looper)]
        return [self.looper.send_order(req) for req in req_list if req.volume != 0]

    def cancel(self, id: Text, origin: [BarData, TickData, TradeData, OrderData, PositionData] = None, **kwargs):
        if "." in id:
            orderid = id.split(".")[1]
        if origin is None:
            exchange = kwargs.get("exchange")
            if isinstance(exchange, Exchange):
                exchange = exchange.value
            local_symbol = kwargs.get("local_symbol")
        elif origin:
            exchange = origin.exchange.value
            local_symbol = origin.local_symbol

        if origin is None and len(kwargs) == 0:
            """ 如果两个都不传"""
            order = self.looper.get_order(id)
            if not order:
                print("找不到订单啦... 撤不了哦")
                return None
            exchange = order.exchange.value
            local_symbol = order.local_symbol
        req = helper.generate_cancel_req_by_str(order_id=orderid, exchange=exchange, symbol=local_symbol)
        return self.looper.cancel_order(req)

    def cancel_all(self):
        return self.looper.cancel_all()

    @staticmethod
    def get_req(local_symbol, direction, volume: int, looper) -> List:
        """
        generate the offset and volume
        生成平仓所需要的offset和volume
         """

        def cal_req(position, volume, looper) -> List:
            # 判断是否为上期所或者能源交易所 / whether the exchange is SHFE or INE
            if position.exchange.value not in looper.params["today_exchange"]:
                return [[Offset.CLOSE, volume]]

            if looper.params["close_pattern"] == "today":
                # 那么先判断今仓数量是否满足volume /
                td_volume = position.volume - position.yd_volume
                if td_volume >= volume:
                    return [[Offset.CLOSETODAY, volume]]
                else:
                    return [[Offset.CLOSETODAY, td_volume],
                            [Offset.CLOSEYESTERDAY, volume - td_volume]] if td_volume != 0 else [
                        [Offset.CLOSEYESTERDAY, volume]]

            elif looper.params["close_pattern"] == "yesterday":
                if position.yd_volume >= volume:
                    """如果昨仓数量要大于或者等于需要平仓数目 那么直接平昨"""
                    return [[Offset.CLOSEYESTERDAY, volume]]
                else:
                    """如果昨仓数量要小于需要平仓数目 那么优先平昨再平今"""
                    return [[Offset.CLOSEYESTERDAY, position.yd_volume],
                            [Offset.CLOSETODAY, volume - position.yd_volume]] if position.yd_volume != 0 else [
                        [Offset.CLOSETODAY, volume]]
            else:
                raise ValueError("异常配置, ctpbee只支持today和yesterday两种优先模式")

        position: PositionData = looper.account.position_manager.get_position_by_ld(local_symbol, direction)
        if not position:
            msg = f"{local_symbol}在{direction.value}上无仓位"
            warn(msg)
            return []
        if position.volume < volume:
            msg = f"{local_symbol}在{direction.value}上仓位不足, 平掉当前 {direction.value} 的所有持仓, 平仓数量: {position.volume}"
            warn(msg)
            return cal_req(position, position.volume, looper)
        else:
            return cal_req(position, volume, looper)


class LocalLooper():
    message_box = {
        -1: "超出下单限制",
        -2: "超出涨跌价格",
        -3: "未成交",
        -4: "资金不足"
    }

    def __init__(self, logger, risk=None):
        """ 需要构建完整的成交回报以及发单报告,在account里面需要存储大量的存储 """

        # 活跃报单数量
        self.change_month_record = {}
        self.pending = []

        self.sessionid = random.randint(1000, 10000)
        self.frontid = random.randint(10001, 500000)

        # 日志输出器
        self.logger = logger
        # 策略池子
        self.strategy_mapping = dict()
        # 覆盖里面的action和logger属性
        # 涨跌停价格
        self.upper_price = 99999
        self.drop_price = 0

        # 风控/risk control todo:完善
        self.risk = risk
        self.params = dict(
            deal_pattern="match",
            single_order_limit=10,
            single_day_limit=100,
            today_exchange=['INE', "SHFE"]
        )
        # 账户属性
        self.account = Account(self)
        self.order_ref = 0

        # 发单的ref集合
        self.order_ref_set = set()
        # 已经order_id ---- 成交单
        self.traded_order_mapping = {}
        # 已经order_id --- 报单
        self.order_id_pending_mapping = {}

        # 当日成交笔数, 需要如果是第二天的数据，那么需要被清空
        self.today_volume = 0

        self.pre_close_price = dict()
        # 所有的报单数量
        self.order_buffer = dict()

        self.date = None
        # 行情
        self.data_entity = None
        self.if_next_day = False
        self.data_type = "bar"

        self.price_mapping = dict()
        # 仓位详细
        self.position_detail = dict()
        self.action = Action(self)

    def get_trades(self):
        return list(self.traded_order_mapping.values())

    def update_strategy(self, strategy):
        setattr(strategy, "action", self.action)
        setattr(strategy, "logger", self.logger)
        setattr(strategy, "info", self.logger.info)
        setattr(strategy, "debug", self.logger.debug)
        setattr(strategy, "error", self.logger.error)
        setattr(strategy, "warning", self.logger.warning)
        setattr(strategy, "app", self)
        self.strategy_mapping[strategy.name] = strategy

    def enable_extension(self, name):
        if name in self.strategy_mapping.keys():
            self.strategy_mapping.get(name).active = True
        else:
            return

    def suspend_extension(self, name):
        if name in self.strategy_mapping.keys():
            self.strategy_mapping.get(name).active = False
        else:
            return

    def update_risk(self, risk):
        self.risk = risk

    def _generate_order_data_from_req(self, req: OrderRequest):
        """ 将发单请求转换为发单数据 """
        self.order_ref += 1
        order_id = f"{self.frontid}-{self.sessionid}-{self.order_ref}"
        return req._create_order_data(gateway_name="looper", order_id=order_id, time=self.datetime)

    def _generate_trade_data_from_order(self, order_data: OrderData):
        """ 将orderdata转换成成交单 """
        p = TradeData(price=order_data.price, istraded=order_data.volume, volume=order_data.volume,
                      tradeid=str(uuid.uuid1()), offset=order_data.offset, direction=order_data.direction,
                      gateway_name=order_data.gateway_name, order_time=order_data.time, time=self.datetime,
                      order_id=order_data.order_id, symbol=order_data.symbol, exchange=order_data.exchange)
        return p

    def send_order(self, order_req: OrderRequest):
        """ 发单的操作 """
        if order_req.volume == 0:
            return 0
        return self.intercept_gateway(order_req)

    def _cancel(self, cancel_req):
        """ 撤单机制 """
        self.intercept_gateway(cancel_req)

    def cancel(self, order_id):
        for x in self.pending:
            if x.order_id == order_id:
                self.pending.remove(x)
                return 1
        return 0

    def cancel_all(self):
        self.pending.clear()
        return 1

    def intercept_gateway(self, data):
        """ 拦截网关 同时这里应该返回相应的水平"""
        if isinstance(data, OrderRequest):
            """ 发单请求处理 """
            order_data = self._generate_order_data_from_req(data)

            if self.account.is_traded(order=order_data):
                self.pending.append(order_data)
                self.account.update_account_from_order(order_data)
                return 1
            else:
                self.logger.info("报单可用不足")
                self.logger.debug(f"close_profit: {self.account.close_profit}")
                self.logger.debug(f"margin: {self.account.margin}")
                self.logger.debug(f"pre_balance: {self.account.pre_balance}")
                self.logger.debug(f"float_pnl: {self.account.float_pnl}")
                self.logger.debug(f"frozen_margin: {self.account.frozen_margin}")
                self.logger.debug(f"available: {self.account.available}")
                return 0
        if isinstance(data, CancelRequest):
            """ 撤单请求处理 
            """
            for order in self.pending:
                if data.order_id == order.order_id:
                    order = deepcopy(order)
                    [api(order) for api in self.strategy_mapping.values()]
                    self.pending.remove(order)
                    self.account.pop_order(order)
                    return 1
            return 0

    def match_deal(self):
        """ 撮合成交
            维护一个返回状态
            -1: 超出下单限制
            -2: 超出涨跌价格
            -3: 未成交
            -4: 资金不足
            p : 成交回报
            todo: 处理冻结 ??
        """
        for data in self.pending:
            px = "".join(filter(str.isalpha, data.local_symbol))
            nx = "".join(filter(str.isalpha, self.data_entity.local_symbol))
            if nx != px:  # 针对多品种，实现拆分。 更新当前的价格，确保多个
                continue
            if self.params.get("deal_pattern") == "match":
                """ 撮合成交 """
                # todo: 是否可以模拟一定量的市场冲击响应？ 以靠近更加逼真的回测效果 ？？？？
                if self.account.is_traded(data):
                    """ 调用API生成成交单 """
                    # 同时这里需要处理是否要进行
                    trade = self._generate_trade_data_from_order(data)
                    self.logger.info(
                        f"--> {trade.local_symbol} 成交时间: {str(trade.time)}, 成交价格{str(trade.price)}, 成交笔数: {str(trade.volume)},"
                        f" 成交方向: {str(trade.direction.value)}，行为: {str(trade.offset.value)}, "
                        f"账户净值: {self.account.balance} 保证金: {self.account.margin} 账户剩余可用: {self.account.available}  此时队列中的单子: {len(self.pending)}")
                    self.account.update_trade(trade)
                    """ 调用strategy的on_trade """
                    self.pending.remove(data)
                    data.status = Status.ALLTRADED
                    [api(deepcopy(data)) for api in self.strategy_mapping.values()]
                    [api(trade) for api in self.strategy_mapping.values()]
                    self.traded_order_mapping[trade.order_id] = trade
                    self.today_volume += data.volume
                else:
                    print("单子没成交哦")
                continue

            elif self.params.get("deal_pattern") == "price":
                """ 见价成交 """
                # 先判断价格和手数是否满足限制条件
                if data.price < self.drop_price or data.price > self.upper_price:
                    """ 超出涨跌价格 """
                    continue
                # 进行成交判断
                long_c = self.data_entity.low_price if self.data_type == "bar" else self.data_entity.ask_price_1
                short_c = self.data_entity.high_price if self.data_type == "bar" is not None else self.data_entity.bid_price_1
                # long_b = self.data_entity.open_price if self.data_type == "bar" is not None else long_c
                # short_b = self.data_entity.open_price if self.data_type == "bar" is not None else short_c
                long_cross = data.direction == Direction.LONG and 0 < long_c <= data.price
                short_cross = data.direction == Direction.SHORT and data.price <= short_c and short_c > 0
                if long_cross:
                    """ 判断账户资金是否足以支撑成交 """
                    if self.account.is_traded(data):
                        """ 调用API生成成交单 """
                        # 同时这里需要处理是否要进行
                        trade = self._generate_trade_data_from_order(data)
                        self.logger.info(
                            f"成交时间: {str(trade.time)}, 成交价格{str(trade.price)}, 成交笔数: {str(trade.volume)},"
                            f" 成交方向: {str(trade.direction.value)}，行为: {str(trade.offset.value)}")
                        self.account.update_trade(trade)
                        """ 调用strategy的on_trade """
                        self.pending.remove(data)
                        data.status = Status.ALLTRADED
                        [api(deepcopy(data)) for api in self.strategy_mapping.values()]
                        [api(trade) for api in self.strategy_mapping.values()]
                        self.traded_order_mapping[trade.order_id] = trade
                        self.today_volume += data.volume
                if short_cross:
                    if self.account.is_traded(data):
                        """ 调用API生成成交单 """
                        # 同时这里需要处理是否要进行
                        trade = self._generate_trade_data_from_order(data)
                        self.logger.info(
                            f"成交时间: {str(trade.time)}, 成交价格{str(trade.price)}, 成交笔数: {str(trade.volume)},"
                            f" 成交方向: {str(trade.direction.value)}，行为: {str(trade.offset.value)}")
                        self.account.update_trade(trade)
                        """ 调用strategy的on_trade """
                        self.pending.remove(data)
                        data.status = Status.ALLTRADED
                        [api(deepcopy(data)) for api in self.strategy_mapping.values()]
                        [api(trade) for api in self.strategy_mapping.values()]
                        self.traded_order_mapping[trade.order_id] = trade
                        self.today_volume += data.volume
                    continue
                else:
                    """ 当前账户不足以支撑成交 """
                    continue
            else:
                raise TypeError("未支持的成交机制")

    def init_params(self, params):
        """ 回测参数设置 """
        self.params.update(params)
        """ 更新接口参数设置 """
        self.params.update(params)
        """ 更新账户策略参数 """

        self.account.update_params(params)

    def __init_params(self, params):
        """ 初始化参数设置  """
        if not isinstance(params, dict):
            raise AttributeError("回测参数类型错误，请检查是否为字典")

        [strategy.init_params(params.get("strategy")) for strategy in self.strategy_mapping.values()]
        self.init_params(params.get("looper"))

    @staticmethod
    def auth_time(time):
        if 15 < time.hour <= 20 or 3 <= time.hour <= 8:
            return False
        else:
            return True

    def __call__(self, *args, **kwargs):
        """ 回测周期 """
        entity, params = args
        # 日期不相等时,　更新前日结算价格
        if self.account.date is None:
            self.account.date = self.date
        if self.date is None:
            self.date = entity.datetime.date()
        if not self.auth_time(entity.datetime):
            return
        self.data_type = entity.type
        # 回测的时候自动更新策略的日期
        if entity.datetime.hour > 21:
            dt = entity.datetime + timedelta(days=1)
        else:
            dt = entity.datetime
        [setattr(x, "date", str(dt.date())) for x in self.strategy_mapping.values()]
        self.__init_params(params)
        try:
            seconds = (entity.datetime - self.datetime).seconds
            if seconds >= 60 * 60 * 4 and (entity.datetime.hour >= 21 or (
                    (14 <= self.datetime.hour <= 15) and entity.datetime.date() != self.datetime.date())):
                self.logger.warning("结算数据:  " + str(self.account.date))
                self.account.settle(entity.datetime.date())

                if self.data_entity is None:
                    self.pre_close_price[
                        self.data_entity.local_symbol] = entity.close_price if entity.type == "bar" else entity.last_price
                else:
                    self.pre_close_price[
                        self.data_entity.local_symbol] = self.data_entity.close_price if entity.type == "bar" \
                        else self.data_entity.last_price
                #  结算完触发初始化函数
                [x.on_init(entity) for x in self.strategy_mapping.values()]
        except KeyError:
            pass
        except AttributeError:
            pass
        self.data_entity = entity
        self.change_month_record["".join(filter(str.isalpha, entity.local_symbol.split(".")[0]))] = entity
        # 维护一个最新的价格
        self.price_mapping[self.data_entity.local_symbol] = self.data_entity.close_price if entity.type == "bar" \
            else self.data_entity.last_price
        if self.pre_close_price.get(self.data_entity.local_symbol) is None:
            self.pre_close_price[
                self.data_entity.local_symbol] = self.data_entity.last_price if entity.type == "tick" else self.data_entity.close_price
        self.datetime = entity.datetime
        self.match_deal()

        if entity.type == "tick":
            [api(entity) for api in self.strategy_mapping.values()]
            self.account.position_manager.update_tick(self.data_entity,
                                                      self.pre_close_price[self.data_entity.local_symbol])
        if entity.type == "bar":
            [api(entity) for api in self.strategy_mapping.values()]
            self.account.position_manager.update_bar(self.data_entity,
                                                     self.pre_close_price[self.data_entity.local_symbol])
        # 更新接口的日期
        self.date = entity.datetime.date()
        # 穿过接口日期检查
        self.account.via_aisle()

    def get_entity_from_alpha(self, alpha):
        return self.change_month_record.get(alpha)
