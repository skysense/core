from connectivity.bitstamp_api import BitstampAPI

if __name__ == '__main__':
    print('Mass canceling all orders.')
    market_api = BitstampAPI()
    print(market_api.open_orders())
    market_api.mass_cancel()
