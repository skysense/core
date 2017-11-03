import json
import logging
import os

from connectivity import api
from helpers.singleton_observable import SingletonObservable


class BitstampAPI(SingletonObservable):
    _instance = None

    def __init__(self):
        super().__init__(BitstampAPI)
        self.logger = logging.getLogger('BitstampAPI')
        for credential_filename in ['credentials.json', '../credentials.json']:
            if os.path.isfile(credential_filename):
                with open(credential_filename, 'r') as r:
                    self.credentials = json.load(r)
                    break
        self.c = self.credentials['CLIENT_ID']
        self.k = self.credentials['API_KEY']
        self.s = self.credentials['API_SECRET']
        self.ticker_headers = ['high', 'last', 'timestamp', 'bid', 'vwap', 'volume', 'low', 'ask', 'open']
        self.last_polled_prices = None

        self.logger.info('CLIENT_ID  (truncated) = {}[...]'.format(self.c[0:3]))
        self.logger.info('API_KEY    (truncated) = {}[...]'.format(self.k[0:10]))
        self.logger.info('API_SECRET (truncated) = {}[...]'.format(self.s[0:10]))

    def buy_limit_order(self, amount, price):
        return api.buy_limit_order(self.c, self.k, self.s, amount, price)

    def cancel_order(self, order_id):
        return api.cancel_order(self.c, self.k, self.s, order_id)

    def order_status(self, order_id):
        return api.order_status(self.c, self.k, self.s, order_id)

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

    @staticmethod
    def ticker():
        return api.ticker()

    def poll(self):
        prices = BitstampAPI.ticker()
        if prices != self.last_polled_prices:  # == works even on Decimal.
            # prices have been updated!
            self.last_polled_prices = prices
            return {'key': 'price_update', 'ticker': self.last_polled_prices}
        return None

    def mass_cancel(self):
        for open_order in self.open_orders():
            self.cancel_order(open_order['id'])

    def terminate(self):
        super().terminate()
        self.logger.info('{0} received a termination call. Will mass cancel all the opened orders.'.format(str(self)))
        self.logger.info('Going to shutdown.')
        self.mass_cancel()
        open_orders = self.open_orders()

        if len(open_orders) == 0:
            self.logger.info('SUCCESS! No more open orders were found.')
