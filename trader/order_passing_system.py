import logging

from constants import MAX_NUMBER_OF_OUTSTANDING_ORDERS_ALLOWED


class OrderPassingSystem:
    def __init__(self, bitstamp_api, throttle):
        self.bitstamp_api = bitstamp_api
        self.throttle = throttle
        self.logger = logging.getLogger('OrderManager')

    def send_buy_order(self, amount, price=None):

        # will throw an exception if invalid.
        self.throttle.check_validity()

        num_open_orders = len(self.bitstamp_api.open_orders())
        if num_open_orders > MAX_NUMBER_OF_OUTSTANDING_ORDERS_ALLOWED:
            raise Exception('Limit of open orders exceeded. Cannot open more orders.')

        if price is None:
            response = self.bitstamp_api.buy_market_order(amount)
        else:
            response = self.bitstamp_api.buy_limit_order(amount, price)

        return response

    def send_sell_order(self, amount, price=None):

        # will throw an exception if invalid.
        self.throttle.check_validity()

        if price is None:
            response = self.bitstamp_api.sell_market_order(amount)
        else:
            response = self.bitstamp_api.sell_limit_order(amount, price)
        return response

    def send_mass_cancel(self):
        self.logger.info('{0} received a termination call. Will mass cancel all the opened orders.'.format(str(self)))
        self.logger.info('Going to shutdown.')
        self.bitstamp_api.mass_cancel()

    def poll(self):
        raise NotImplementedError('Nothing to implement here.')
