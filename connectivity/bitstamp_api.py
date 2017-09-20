import json
import logging

from connectivity import api
from connectivity.observable import Observable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BitstampAPI(Observable):
    def __init__(self):
        super().__init__()
        self.credentials = json.load(open('../credentials.json', 'r'))
        self.c = self.credentials['CLIENT_ID']
        self.k = self.credentials['API_KEY']
        self.s = self.credentials['API_SECRET']
        self.ticker_headers = ['high', 'last', 'timestamp', 'bid', 'vwap', 'volume', 'low', 'ask', 'open']
        self.last_polled_prices = None

        logging.info('CLIENT_ID  (truncated) = {}[...]'.format(self.c[0:3]))
        logging.info('API_KEY    (truncated) = {}[...]'.format(self.k[0:10]))
        logging.info('API_SECRET (truncated) = {}[...]'.format(self.s[0:10]))

    def buy_limit_order(self, amount, price):
        return api.buy_limit_order(self.c, self.k, self.s, amount, price)

    def api_cancel_order(self, order_id):
        return api.cancel_order(self.c, self.k, self.s, order_id)

    def sell_limit_order(self, amount, price):
        return api.sell_limit_order(self.c, self.k, self.s, amount, price)

    def buy_market_order(self, amount):
        return api.buy_market_order(self.c, self.k, self.s, amount)

    def sell_market_order(self, amount):
        return api.sell_market_order(self.c, self.k, self.s, amount)

    def user_transactions(self):
        return api.user_transactions(self.c, self.k, self.s)

    @staticmethod
    def order_book():
        return api.order_book()

    def account_balance(self):
        return api.account_balance(self.c, self.k, self.s)

    def open_orders(self):
        return api.open_orders(self.c, self.k, self.s)

    @staticmethod
    def compare_ticker_prices(p1, p2):
        return p1 == p2

    def poll(self):
        prices = api.ticker()
        if prices != self.last_polled_prices:  # == works even on Decimal.
            # prices have been updated!
            self.last_polled_prices = prices
            return {'key': 'price_update', 'ticker': self.last_polled_prices}
        return None
