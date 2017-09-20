import logging
from datetime import datetime

from connectivity.singleton_observable import SingletonObservable
from model.model import TIME_HORIZON

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)20s - %(levelname)s - %(message)s')


class UnwindManager(SingletonObservable):
    _instance = None

    def __init__(self, bitstamp_api, persistence):
        super().__init__(UnwindManager)
        self.bitstamp_api = bitstamp_api
        self.persistence = persistence
        self.polling_interval = 15  # In seconds. This API call is cached for 10 seconds.
        self.trading_time_horizon = TIME_HORIZON  # In seconds. very important parameter!

    def poll(self):
        # we pull because we want to be synchronized. Keeping a collection in memory is the best way to be de-sync
        # from the market.
        orders = self.persistence.enrich_persisted_orders_with_market_statuses(
            self.persistence.read_from_persistence())

        for order in orders:
            if order['status']['market trade'] == 'market trade' and order['status']['status'] == 'Finished':
                ts = datetime.strptime(order['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                if ts + TIME_HORIZON > datetime.now():
                    logging.info(
                        'Outstanding order initiated at {0} with Order ID = {1}. '
                        'Will going to close it. Full order is = {2}'.format(ts, order['id'], order))
                    self.bitstamp_api.sell_market_order(order['amount'])
