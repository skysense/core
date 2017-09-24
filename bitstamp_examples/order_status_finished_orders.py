import logging

from connectivity.bitstamp_api import BitstampAPI

LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

bitstamp = BitstampAPI()

order_id_buy = '320464858'
order_id_sell = '320466285'

bitstamp.order_status(order_id_buy)
bitstamp.order_status(order_id_sell)

"""
2017-09-24 23:15:27,404 -     BitstampAPI - INFO - [3038] TO BITSTAMP : https://www.bitstamp.net/api/order_status/ {'id': '320464858', 'key': '***', 'signature': '***', 'nonce': '1506262527404037'}
2017-09-24 23:15:28,162 -     BitstampAPI - INFO - [3038] FROM BITSTAMP : {'status': 'Finished', 'transactions': [{'fee': '0.03000000', 'price': '3083.26000000', 'datetime': '2017-09-24 11:09:39', 'btc': '0.00300000', 'tid': 22155667, 'type': 2, 'eur': '9.24978000'}]}
2017-09-24 23:15:28,162 -     BitstampAPI - INFO - [2328] TO BITSTAMP : https://www.bitstamp.net/api/order_status/ {'id': '320466285', 'key': '***', 'signature': '***', 'nonce': '1506262528162275'}
2017-09-24 23:15:28,777 -     BitstampAPI - INFO - [2328] FROM BITSTAMP : {'status': 'Finished', 'transactions': [{'fee': '0.03000000', 'price': '3073.15000000', 'datetime': '2017-09-24 11:10:27', 'btc': '0.00300000', 'tid': 22155681, 'type': 2, 'eur': '9.21945000'}]}
"""
