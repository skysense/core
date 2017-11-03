from connectivity.api import USER_TRANSACTIONS_TYPE_MARKET_TRADE
from constants import TIME_HORIZON
from helpers.singleton_observable import SingletonObservable

# TODO: test it!

"""
The way I see it is:
- every hour we request the market.
- we can buy and sell.
- buy 0.01. Balance is 0.01.
- buy 0.01. Balance is 0.02.
- sell 0.01. Balance is 0.01.
- buy 0.01. Balance is 0.02.
- sell 0.01. Balance is 0.01.
- sell 0.01. Balance is 0.00.
- sell 0.01. Balance is 0.00.

"""


class UnwindManager(SingletonObservable):
    _instance = None

    def __init__(self, bitstamp_api):
        super().__init__(UnwindManager)
        self.bitstamp_api = bitstamp_api
        self.polling_interval = 15  # In seconds. This API call is cached for 10 seconds.
        self.trading_time_horizon = TIME_HORIZON  # In seconds. very important parameter!

    def poll(self):
        # we poll because we want to be synchronized.
        #  Keeping a collection in memory is the best way to be de-sync
        # from the market.
        user_transactions = self.bitstamp_api.user_transactions()
        if len(user_transactions) > 0:
            last_transaction = user_transactions[0]
            if str(last_transaction['type']) == str(USER_TRANSACTIONS_TYPE_MARKET_TRADE):
                pass


                # for order in orders:
                #     if order['status']['market trade'] == 'market trade' and order['status']['status'] == 'Finished':
                #         ts = datetime.strptime(order['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                #         if ts + TIME_HORIZON > datetime.now():
                #             self.logger.info(
                #                 'Outstanding order initiated at {0} with Order ID = {1}. '
                #                 'Will going to close it. Full order is = {2}'.format(ts, order['id'], order))
                #             self.bitstamp_api.sell_market_order(order['amount'])
