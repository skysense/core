class OrderManagement:
    def __init__(self, bitstamp_api, throttle):
        self.bitstamp_api = bitstamp_api
        self.throttle = throttle
        self.open_orders = []

    def send_buy_order(self, amount, price=None):

        self.throttle.check_validity()  # will throw an exception if invalid.

        if price is None:
            response = self.bitstamp_api.buy_market_order(amount)
        else:
            response = self.bitstamp_api.buy_limit_order(amount, price)
        self.open_orders.append(response)
        # do something here.

    def send_sell_order(self, amount, price=None):

        self.throttle.check_validity()  # will throw an exception if invalid.

        if price is None:
            response = self.bitstamp_api.sell_market_order(amount)
        else:
            response = self.bitstamp_api.sell_limit_order(amount, price)
        self.open_orders.append(response)
        # do something here.
