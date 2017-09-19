from trader.bitstamp_api import BitstampAPI

market_api = BitstampAPI()


def run():
    market_api.order_book()


if __name__ == '__main__':
    run()
