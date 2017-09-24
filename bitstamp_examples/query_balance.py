import logging

from connectivity.bitstamp_api import BitstampAPI

LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT)

bitstamp = BitstampAPI()

print(bitstamp.account_balance())

# REQUEST
# https://www.bitstamp.net/api/v2/balance/ 
"""
{'key': '***',
 'signature': '***',
 'nonce': '1506248716150761'}
"""

# RESPONSE
"""
{'btc_available': '0.00000000',
 'btc_balance': '0.00000000',
 'btc_reserved': '0.00000000',
 'btceur_fee': '0.25',
 'btcusd_fee': '0.25',
 'eth_available': '0.00000000',
 'eth_balance': '0.00000000',
 'eth_reserved': '0.00000000',
 'ethbtc_fee': '0.00',
 'etheur_fee': '0.00',
 'ethusd_fee': '0.00',
 'eur_available': '105.00',
 'eur_balance': '105.00',
 'eur_reserved': '0.00',
 'eurusd_fee': '0.25',
 'ltc_available': '0.00000000',
 'ltc_balance': '0.00000000',
 'ltc_reserved': '0.00000000',
 'ltcbtc_fee': '0.25',
 'ltceur_fee': '0.25',
 'ltcusd_fee': '0.25',
 'usd_available': '0.00',
 'usd_balance': '0.00',
 'usd_reserved': '0.00',
 'xrp_available': '0.00000000',
 'xrp_balance': '0.00000000',
 'xrp_reserved': '0.00000000',
 'xrpbtc_fee': '0.25',
 'xrpeur_fee': '0.25',
 'xrpusd_fee': '0.25'}
"""
