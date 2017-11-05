from constants import TRADING_BITCOIN_QUANTITY_TO_BUY_OR_SELL
from constants import TRADING_BUY_CONFIDENCE_THRESHOLD
from constants import TRADING_SELL_CONFIDENCE_THRESHOLD


def play_buy_order_sound():
    # pip3 install -U pyobjc
    # pip3 install playsound
    try:
        from playsound import playsound
        # playsound('sounds/Coin_Obtained_SFX.wav')
        playsound('sounds/buy.mp3')
    except:
        pass


def play_sell_order_sound():
    # pip3 install -U pyobjc
    # pip3 install playsound
    try:
        from playsound import playsound
        # playsound('sounds/Pipe_Maze_SFX.wav')
        playsound('sounds/sell.mp3')
    except:
        pass


class ModelActionTaker:
    def __init__(self, order_passing_system):
        self.order_passing_system = order_passing_system
        self.order_quantity = TRADING_BITCOIN_QUANTITY_TO_BUY_OR_SELL

    def take_trading_action(self, model_output):
        response = None
        if model_output.buy_confidence > TRADING_BUY_CONFIDENCE_THRESHOLD:
            response = self.order_passing_system.send_buy_order(amount=self.order_quantity)
            play_buy_order_sound()
        elif model_output.sell_confidence > TRADING_SELL_CONFIDENCE_THRESHOLD:
            response = self.order_passing_system.send_sell_order(amount=self.order_quantity)
            play_sell_order_sound()
        return response
