import logging

from connectivity.bitstamp_api import BitstampAPI

LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.INFO,

                    format=LOG_FORMAT)

bitstamp = BitstampAPI()

print(bitstamp.cancel_order(order_id='320407487'))
