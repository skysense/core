
from trader.bitstamp_api import BitstampAPIv1

market_api = BitstampAPIv1()

def run():
    market_api.order_book()

if __name__ == '__main__':
    run()