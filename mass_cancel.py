from connectivity.bitstamp_api import BitstampAPI

market_api = BitstampAPI()
print(market_api.open_orders())

market_api.mass_cancel()
