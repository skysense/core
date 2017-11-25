import logging
import os
from datetime import datetime

ADMIN_PROD_FLAG = False

MODEL_CHECKPOINTS_DIR = 'model_checkpoints/'
MODEL_INPUT_TENSOR_NAME = 'Input/ClosePrices'  # could be several in a very near future
MODEL_OUTPUT_TENSOR_NAME = 'Output/Prediction'

if not ADMIN_PROD_FLAG:
    # Simulation. With Localhost.
    TRADING_MAX_NUMBER_OF_OUTSTANDING_ORDERS_ALLOWED = 1
    TRADING_BITCOIN_QUANTITY_TO_BUY_OR_SELL = 0.001  # in BTC.
    TRADING_MIN_INTERVAL_BETWEEN_TWO_SEND_ORDERS = 0  # seconds
    TRADING_BUY_CONFIDENCE_THRESHOLD = 0.50  # between 0 and 1.
    TRADING_SELL_CONFIDENCE_THRESHOLD = 0.50  # between 0 and 1.
    MODEL_WARM_UP_PHASE_NUM_TICKS = 2  # number of market ticks before we can start to call the model.
    SIMULATOR_REPLAYER_DATA_FILE = '../data_examples/btc_price_2017-09-13T03:45:28+00:00.csv'
    API_URL_V1 = 'http://127.0.0.1:5000/'
    API_URL_V2 = 'http://127.0.0.1:5000/v2/'
    API_URL_V2_TICKER = 'https://www.bitstamp.net/api/v2/'
    TICKER_POLL_INTERVAL_SEC = 5

    # True = simulator replays the file SIMULATOR_REPLAYER_DATA_FILE
    # False = simulator connects to Bitstamp (API_URL_V2_TICKER) and calls ticker() to get RT market data.
    SIMULATOR_USE_REPLAYER = True
else:
    # Production. With Bitstamp.
    TRADING_MAX_NUMBER_OF_OUTSTANDING_ORDERS_ALLOWED = 1
    TRADING_BITCOIN_QUANTITY_TO_BUY_OR_SELL = 0.001  # in BTC.
    TRADING_MIN_INTERVAL_BETWEEN_TWO_SEND_ORDERS = 10  # seconds
    TRADING_BUY_CONFIDENCE_THRESHOLD = 0.95  # between 0 and 1.
    TRADING_SELL_CONFIDENCE_THRESHOLD = 0.95  # between 0 and 1.
    MODEL_WARM_UP_PHASE_NUM_TICKS = 100  # number of market ticks before we can start to call the model.
    API_URL_V1 = 'https://www.bitstamp.net/api/'
    API_URL_V2 = 'https://www.bitstamp.net/api/v2/'
    TICKER_POLL_INTERVAL_SEC = 5

ADMIN_LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

TRADING_DEFAULT_CURRENCY_PAIR = 'btceur'

# deprecated do not use it.
# we don't have a trading horizon now. We just watch the market and make
# some trades whenever there's an opportunity. It's a dynamic time horizon.
DEPRECATED__TRADING_TIME_HORIZON = 3600  # seconds.

if ADMIN_PROD_FLAG:

    if input('Are you sure you want to run in production (Bitstamp.net)? (y/n) ') != 'y':
        exit()

    log_filename = os.path.join('log', 'trading_{0}.log'.format(datetime.now()))
    print('Check the log file {0} if nothing is displayed in the console.'.format(log_filename))
    logging.basicConfig(level=logging.INFO,
                        format=ADMIN_LOG_FORMAT,
                        filename=log_filename)
else:
    logging.basicConfig(level=logging.INFO,
                        format=ADMIN_LOG_FORMAT)
