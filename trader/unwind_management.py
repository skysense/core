from datetime import datetime

from connectivity.observable import Observable
from model.model import TIME_HORIZON


class UnwindManager(Observable):
    def __init__(self, bitstamp_api):
        super().__init__()
        self.bitstamp_api = bitstamp_api
        self.polling_interval = 15  # In seconds. This API call is cached for 10 seconds.
        self.trading_time_horizon = TIME_HORIZON  # In seconds. very important parameter!

    """
    ORDER STATUS
    https://www.bitstamp.net/api/
    This call will be executed on the account (Sub or Main), to which the used API key is bound to.
    Request
    POST	https://www.bitstamp.net/api/order_status/
    Request parameters
    key	API key.
    signature	Signature.
    nonce	Nonce.
    id	Order ID.
    Response (JSON)
    status	In Queue, Open or Finished.
    transactions	Each transaction in dictionary is represented as a list of tid, usd, price, fee, btc, datetime and type (0 - deposit; 1 - withdrawal; 2 - market trade).
        """

    def poll(self):
        # we pull because we want to be synchronized. Keeping a collection in memory is the best way to be de-sync
        # from the market.
        # 	Transaction type: 0 - deposit; 1 - withdrawal; 2 - market trade; 14 - sub account transfer.
        executions = self.bitstamp_api.user_transactions()
        for execution in executions:
            if execution['type'] == 2:
                pass
                # execution
            if execution['datetime'] + self.trading_time_horizon > datetime.now():
                # for now unwinding is reserved to buy orders.
                self.bitstamp_api.sell_market_order()

    # order id comes from the id when placing a market/limit order.

    def add_order_to_unwind(self, order_id, unwind_datetime):
        self.orders_to_unwind[order_id] = unwind_datetime
