class OrderManagement:
    def __init__(self, bitstamp_api):
        self.bitstamp_api = bitstamp_api
        self.open_orders = []

    def send_buy_order(self, amount, price=None):
        if price is None:
            response = self.bitstamp_api.buy_market_order(amount)
        else:
            response = self.bitstamp_api.buy_limit_order(amount, price)
        self.open_orders.append(response)
        # do something here.

    def send_sell_order(self, amount, price=None):
        if price is None:
            response = self.bitstamp_api.sell_market_order(amount)
        else:
            response = self.bitstamp_api.sell_limit_order(amount, price)
        self.open_orders.append(response)
        # do something here.
