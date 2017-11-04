ADMIN_PROD_FLAG = False

if not ADMIN_PROD_FLAG:
    # Simulation. With Localhost.
    TRADING_MAX_NUMBER_OF_OUTSTANDING_ORDERS_ALLOWED = 1
    TRADING_BITCOIN_QUANTITY_TO_BUY_OR_SELL = 0.001  # in BTC.
    TRADING_MIN_INTERVAL_BETWEEN_TWO_SEND_ORDERS = 0  # seconds
    TRADING_BUY_CONFIDENCE_THRESHOLD = 0.5  # between 0 and 1.
    TRADING_SELL_CONFIDENCE_THRESHOLD = 0.5  # between 0 and 1.
    MODEL_WARM_UP_PHASE_NUM_TICKS = 10  # number of market ticks before we can start to call the model.
    SIMULATOR_REPLAYER_DATA_FILE = '../data_examples/btc_price_2017-09-13T03:45:28+00:00.csv'
    API_URL_V1 = 'http://127.0.0.1:5000/'
    API_URL_V2 = 'http://127.0.0.1:5000/v2/'
    TICKER_POLL_INTERVAL_SEC = 5
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
