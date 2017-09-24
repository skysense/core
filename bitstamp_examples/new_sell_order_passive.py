import logging
from decimal import Decimal

from connectivity.bitstamp_api import BitstampAPI

LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO,

                    format=LOG_FORMAT)

bitstamp = BitstampAPI()

ticker = bitstamp.ticker()
print(ticker)

sell_limit_price = ticker['last'] * Decimal(1.2)  # well below.

sell_limit_price = '{0:.2f}'.format(sell_limit_price)
print(sell_limit_price)
amount = 0.003
print('Order size is {} EUR'.format(float(sell_limit_price) * amount))  # minimum 5 EUR it must be!

print(bitstamp.sell_market_order(amount=amount))
# {'status': 'error', 'reason': {'__all__': ['You can only sell 0.00000000 BTC. Check your account balance for details.']}}

# print(bitstamp.sell_limit_order(amount=amount, price=sell_limit_price))
# {'status': 'error', 'reason': {'__all__': ['You have only 0.00000000 BTC available. Check your account balance for details.']}}
