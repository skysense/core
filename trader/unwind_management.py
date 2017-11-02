from datetime import datetime

from constants import TIME_HORIZON
from helpers.singleton_observable import SingletonObservable


# TODO: test it!

class UnwindManager(SingletonObservable):
    _instance = None

    def __init__(self, bitstamp_api, persistence):
        super().__init__(UnwindManager)
        self.bitstamp_api = bitstamp_api
        self.persistence = persistence
        self.polling_interval = 15  # In seconds. This API call is cached for 10 seconds.
        self.trading_time_horizon = TIME_HORIZON  # In seconds. very important parameter!

    def poll(self):
        # we poll because we want to be synchronized.
        #  Keeping a collection in memory is the best way to be de-sync
        # from the market.
        orders = self.persistence.enrich_persisted_orders_with_market_statuses(
            self.persistence.read_from_persistence())

        for order in orders:
            if order['status']['market trade'] == 'market trade' and order['status']['status'] == 'Finished':
                ts = datetime.strptime(order['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                if ts + TIME_HORIZON > datetime.now():
                    self.logger.info(
                        'Outstanding order initiated at {0} with Order ID = {1}. '
                        'Will going to close it. Full order is = {2}'.format(ts, order['id'], order))
                    self.bitstamp_api.sell_market_order(order['amount'])

    def terminate(self):
        super().terminate()
        # orders = self.persistence.enrich_persisted_orders_with_market_statuses(
        #    self.persistence.read_from_persistence())

        # TODO: implement mass cancel
        self.logger.info('{0} received a termination call. Will mass cancel all the opened orders.'.format(str(self)))
        self.logger.error('TODO!')
        self.logger.info('Going to shutdown.')
