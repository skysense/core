import logging
from time import sleep

from connectivity.bitstamp_api import BitstampAPI

LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

bitstamp = BitstampAPI()

amount = 0.003

order = bitstamp.buy_market_order(amount=amount)

order_id = order['id']

try:
    bitstamp.open_orders()
except:
    pass

try:
    bitstamp.order_status(order_id)
except:
    pass

try:
    bitstamp.user_transactions()
except:
    pass

try:
    bitstamp.account_balance()
except:
    pass

sleep(30)
bitstamp.sell_market_order(amount=amount)

try:
    bitstamp.open_orders()
except:
    pass

try:
    bitstamp.order_status(order_id)
except:
    pass

try:
    bitstamp.user_transactions()
except:
    pass

try:
    bitstamp.account_balance()
except:
    pass

"""
2017-09-24 20:09:34,824 -     BitstampAPI - INFO - CLIENT_ID  (truncated) = 864[...]
2017-09-24 20:09:34,826 -     BitstampAPI - INFO - API_KEY    (truncated) = XXHmrWazGk[...]
2017-09-24 20:09:34,826 -     BitstampAPI - INFO - API_SECRET (truncated) = SoHgJv52DX[...]
2017-09-24 20:09:35,798 -     BitstampAPI - INFO - [7926] TO BITSTAMP : https://www.bitstamp.net/api/v2/buy/market/btceur/ {'amount': 0.003, 'key': '***', 'signature': '***', 'nonce': '1506251375795815'}
2017-09-24 20:09:37,297 -     BitstampAPI - INFO - [7926] FROM BITSTAMP : {'price': '3083.26', 'amount': '0.00300000', 'type': '0', 'id': '320464858', 'datetime': '2017-09-24 11:09:38.577458'}
2017-09-24 20:09:40,958 -     BitstampAPI - INFO - [1803] TO BITSTAMP : https://www.bitstamp.net/api/v2/open_orders/all/ {'key': '***', 'signature': '***', 'nonce': '1506251380957991'}
2017-09-24 20:09:41,522 -     BitstampAPI - INFO - [1803] FROM BITSTAMP : []
2017-09-24 20:09:43,558 -     BitstampAPI - INFO - [2623] TO BITSTAMP : https://www.bitstamp.net/api/order_status/ {'id': '320464858', 'key': '***', 'signature': '***', 'nonce': '1506251383558164'}
2017-09-24 20:09:44,670 -     BitstampAPI - INFO - [2623] FROM BITSTAMP : {'status': 'Finished', 'transactions': [{'fee': '0.03000000', 'price': '3083.26000000', 'datetime': '2017-09-24 11:09:39', 'btc': '0.00300000', 'tid': 22155667, 'type': 2, 'eur': '9.24978000'}]}
2017-09-24 20:09:46,605 -     BitstampAPI - INFO - [9798] TO BITSTAMP : https://www.bitstamp.net/api/v2/user_transactions/ {'offset': 0, 'limit': 100, 'sort': 'desc', 'key': '***', 'signature': '***', 'nonce': '1506251386605325'}
2017-09-24 20:09:47,428 -     BitstampAPI - INFO - [9798] FROM BITSTAMP : [{'fee': '0.03', 'order_id': 320464858, 'datetime': '2017-09-24 11:09:39', 'usd': 0.0, 'btc': '0.00300000', 'btc_eur': 3083.26, 'type': '2', 'id': 22155667, 'eur': '-9.25'}, {'fee': '0.00', 'btc_usd': '0.00', 'datetime': '2017-09-22 08:45:10', 'usd': 0.0, 'btc': 0.0, 'type': '0', 'id': 22034181, 'eur': '105.00'}]
2017-09-24 20:09:49,586 -     BitstampAPI - INFO - [4709] TO BITSTAMP : https://www.bitstamp.net/api/v2/balance/ {'key': '***', 'signature': '***', 'nonce': '1506251389585991'}
2017-09-24 20:09:50,545 -     BitstampAPI - INFO - [4709] FROM BITSTAMP : {'btc_available': '0.00300000', 'btc_balance': '0.00300000', 'btc_reserved': '0.00000000', 'btceur_fee': '0.25', 'btcusd_fee': '0.25', 'eth_available': '0.00000000', 'eth_balance': '0.00000000', 'eth_reserved': '0.00000000', 'ethbtc_fee': '0.00', 'etheur_fee': '0.00', 'ethusd_fee': '0.00', 'eur_available': '95.72', 'eur_balance': '95.72', 'eur_reserved': '0.00', 'eurusd_fee': '0.25', 'ltc_available': '0.00000000', 'ltc_balance': '0.00000000', 'ltc_reserved': '0.00000000', 'ltcbtc_fee': '0.25', 'ltceur_fee': '0.25', 'ltcusd_fee': '0.25', 'usd_available': '0.00', 'usd_balance': '0.00', 'usd_reserved': '0.00', 'xrp_available': '0.00000000', 'xrp_balance': '0.00000000', 'xrp_reserved': '0.00000000', 'xrpbtc_fee': '0.25', 'xrpeur_fee': '0.25', 'xrpusd_fee': '0.25'}
2017-09-24 20:10:24,631 -     BitstampAPI - INFO - [6577] TO BITSTAMP : https://www.bitstamp.net/api/v2/sell/market/btceur/ {'amount': 0.003, 'key': '***', 'signature': '***', 'nonce': '1506251424631168'}
2017-09-24 20:10:25,407 -     BitstampAPI - INFO - [6577] FROM BITSTAMP : {'price': '3073.15', 'amount': '0.00300000', 'type': '1', 'id': '320466285', 'datetime': '2017-09-24 11:10:26.917386'}
2017-09-24 20:10:28,425 -     BitstampAPI - INFO - [4682] TO BITSTAMP : https://www.bitstamp.net/api/v2/open_orders/all/ {'key': '***', 'signature': '***', 'nonce': '1506251428425274'}
2017-09-24 20:10:29,205 -     BitstampAPI - INFO - [4682] FROM BITSTAMP : []
2017-09-24 20:10:30,738 -     BitstampAPI - INFO - [5752] TO BITSTAMP : https://www.bitstamp.net/api/order_status/ {'id': '320464858', 'key': '***', 'signature': '***', 'nonce': '1506251430737872'}
2017-09-24 20:10:31,777 -     BitstampAPI - INFO - [5752] FROM BITSTAMP : {'status': 'Finished', 'transactions': [{'fee': '0.03000000', 'price': '3083.26000000', 'datetime': '2017-09-24 11:09:39', 'btc': '0.00300000', 'tid': 22155667, 'type': 2, 'eur': '9.24978000'}]}
2017-09-24 20:10:32,537 -     BitstampAPI - INFO - [6481] TO BITSTAMP : https://www.bitstamp.net/api/v2/user_transactions/ {'offset': 0, 'limit': 100, 'sort': 'desc', 'key': '***', 'signature': '***', 'nonce': '1506251432536492'}
2017-09-24 20:10:33,213 -     BitstampAPI - INFO - [6481] FROM BITSTAMP : [{'fee': '0.03000000', 'order_id': 320466285, 'datetime': '2017-09-24 11:10:27', 'usd': 0.0, 'btc': '-0.00300000', 'btc_eur': 3073.15, 'type': '2', 'id': 22155681, 'eur': '9.22'}, {'fee': '0.03', 'order_id': 320464858, 'datetime': '2017-09-24 11:09:39', 'usd': 0.0, 'btc': '0.00300000', 'btc_eur': 3083.26, 'type': '2', 'id': 22155667, 'eur': '-9.25'}, {'fee': '0.00', 'btc_usd': '0.00', 'datetime': '2017-09-22 08:45:10', 'usd': 0.0, 'btc': 0.0, 'type': '0', 'id': 22034181, 'eur': '105.00'}]
2017-09-24 20:10:34,024 -     BitstampAPI - INFO - [2838] TO BITSTAMP : https://www.bitstamp.net/api/v2/balance/ {'key': '***', 'signature': '***', 'nonce': '1506251434024463'}
2017-09-24 20:10:35,657 -     BitstampAPI - INFO - [2838] FROM BITSTAMP : {'btc_available': '0.00000000', 'btc_balance': '0.00000000', 'btc_reserved': '0.00000000', 'btceur_fee': '0.25', 'btcusd_fee': '0.25', 'eth_available': '0.00000000', 'eth_balance': '0.00000000', 'eth_reserved': '0.00000000', 'ethbtc_fee': '0.00', 'etheur_fee': '0.00', 'ethusd_fee': '0.00', 'eur_available': '104.90', 'eur_balance': '104.90', 'eur_reserved': '0.00', 'eurusd_fee': '0.25', 'ltc_available': '0.00000000', 'ltc_balance': '0.00000000', 'ltc_reserved': '0.00000000', 'ltcbtc_fee': '0.25', 'ltceur_fee': '0.25', 'ltcusd_fee': '0.25', 'usd_available': '0.00', 'usd_balance': '0.00', 'usd_reserved': '0.00', 'xrp_available': '0.00000000', 'xrp_balance': '0.00000000', 'xrp_reserved': '0.00000000', 'xrpbtc_fee': '0.25', 'xrpeur_fee': '0.25', 'xrpusd_fee': '0.25'}

Process finished with exit code 0

"""
