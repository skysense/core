MAX_NUMBER_OF_OUTSTANDING_ORDERS_ALLOWED = 1


class OrderManager:
    def __init__(self, bitstamp_api, throttle, persistence):
        self.bitstamp_api = bitstamp_api
        self.throttle = throttle
        self.persistence = persistence

    @staticmethod
    def check_outstanding_orders(orders):
        num_open_orders = 0
        for order in orders:
            if order['status'] == 'In Queue' or order['status'] == 'Open':
                num_open_orders += 1
        return num_open_orders

    def send_buy_order(self, amount, price=None):

        # will throw an exception if invalid.
        self.throttle.check_validity()

        # Will be slow once the persistence is big.
        orders = self.persistence.enrich_persisted_orders_with_market_statuses(self.persistence.read_from_persistence())

        num_open_orders = OrderManager.check_outstanding_orders(orders)
        if num_open_orders > MAX_NUMBER_OF_OUTSTANDING_ORDERS_ALLOWED:
            raise Exception('Limit of open orders exceeded. Cannot open more orders.')

        if price is None:
            response = self.bitstamp_api.buy_market_order(amount)
        else:
            response = self.bitstamp_api.buy_limit_order(amount, price)
        return response

    def send_sell_order(self, amount, price=None):
        raise Exception('Not used now. We only send buy orders and we have a mechanism to unwind them.')
