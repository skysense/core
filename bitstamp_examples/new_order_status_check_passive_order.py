import logging
from decimal import Decimal

from connectivity.bitstamp_api import BitstampAPI

LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO,

                    format=LOG_FORMAT)

bitstamp = BitstampAPI()

ticker = bitstamp.ticker()
print(ticker)

buy_limit_price = ticker['last'] * Decimal(0.8)  # well below.

buy_limit_price = '{0:.2f}'.format(buy_limit_price)
print(buy_limit_price)
amount = 0.003
print('Order size is {} EUR'.format(float(buy_limit_price) * amount))  # minimum 5 EUR it must be!

print(bitstamp.account_balance())

order = bitstamp.buy_limit_order(amount=amount, price=buy_limit_price)

print(bitstamp.account_balance())  # 'eur_available': '97.57', 'eur_balance': '105.00'

# <class 'list'>: [{'price': Decimal('2470.22'), 'currency_pair': 'BTC/EUR',
# 'datetime': datetime.datetime(2017, 9, 24, 10, 50, 50), 'amount': Decimal('0.00300000'),
# 'type': '0', 'id': '320422620'}]
print(bitstamp.open_orders())

order_id = order['id']

print(bitstamp.order_status(order_id))  # {'status': 'Open', 'transactions': []}

print(bitstamp.cancel_order(order_id))
