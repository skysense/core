import logging
from decimal import Decimal

from connectivity.bitstamp_api import BitstampAPI

LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO,

                    format=LOG_FORMAT)

bitstamp = BitstampAPI()

ticker = bitstamp.ticker()
print(ticker)

# REQUEST
# TO BITSTAMP : https://www.bitstamp.net/api/v2/ticker/btceur/ {}

# ANSWER
"""
{'high': '3217.17',
 'last': '3094.11',
 'timestamp': '1506249009',
 'bid': '3087.69',
 'vwap': '3149.80',
 'volume': '1148.62901405',
 'low': '3050.50',
 'ask': '3094.11',
 'open': '3174.97'}
"""

# try:
#     print(bitstamp.cancel_order(order_id='hello_33'))
# except:
#     pass

# REQUEST
# TO BITSTAMP : https://www.bitstamp.net/api/v2/cancel_order/ {'id': 'hello_33', 'key': '***', 'signature': '***', 'nonce': '1506249164703340'}
# FROM BITSTAMP :
"""
{'error': 'Invalid order id'}
"""

buy_limit_price = ticker['last'] * Decimal(0.8)  # well below.

buy_limit_price = '{0:.2f}'.format(buy_limit_price)
print(buy_limit_price)
amount = 0.003
print('Order size is {} EUR'.format(float(buy_limit_price) * amount))  # minimum 5 EUR it must be!

# price = 2471.61, amount = 0.003, way = buy
print(bitstamp.buy_limit_order(amount=amount, price=buy_limit_price))

# 2017-09-24 19:44:06,178 -     BitstampAPI - INFO - [8276] FROM BITSTAMP :
#

"""
{'price': '2471.61', 
'amount': '0.00300000', 
'type': '0', 
'id': '320407487', 
'datetime': '2017-09-24 10:44:07.349503'}
"""

# {'price': Decimal('2471.61'), 'amount': Decimal('0.00300000'), 'type': '0', 'id': '320407487', 'datetime': datetime.datetime(2017, 9, 24, 10, 44, 7)}
