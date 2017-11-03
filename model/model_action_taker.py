from constants import TRADING_BITCOIN_QUANTITY_TO_BUY_OR_SELL
from constants import BUY_CONFIDENCE_THRESHOLD
from constants import SELL_CONFIDENCE_THRESHOLD


class ModelActionTaker:
    def __init__(self, order_passing_system):
        self.order_passing_system = order_passing_system
        self.order_quantity = TRADING_BITCOIN_QUANTITY_TO_BUY_OR_SELL

    def take_trading_action(self, model_output):
        if model_output.buy_confidence > BUY_CONFIDENCE_THRESHOLD:
            return self.order_passing_system.send_buy_order(amount=self.order_quantity)
        elif model_output.sell_confidence > SELL_CONFIDENCE_THRESHOLD:
            return self.order_passing_system.send_sell_order(amount=self.order_quantity)
        else:
            return None
