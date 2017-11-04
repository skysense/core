TRADING_DEFAULT_CURRENCY_PAIR = 'btceur'

TRADING_MAX_NUMBER_OF_OUTSTANDING_ORDERS_ALLOWED = 1

TRADING_BITCOIN_QUANTITY_TO_BUY_OR_SELL = 0.001  # in BTC.

TRADING_MIN_INTERVAL_BETWEEN_TWO_SEND_ORDERS = 300  # seconds

TRADING_BUY_CONFIDENCE_THRESHOLD = 0.999  # between 0 and 1.

TRADING_SELL_CONFIDENCE_THRESHOLD = 0.999  # between 0 and 1.

MODEL_WARM_UP_PHASE_NUM_TICKS = 100  # number of market ticks before we can start to call the model.

ADMIN_LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

ADMIN_PROD_FLAG = False

# deprecated do not use it.
# we don't have a trading horizon now. We just watch the market and make
# some trades whenever there's an opportunity. It's a dynamic time horizon.
DEPRECATED__TRADING_TIME_HORIZON = 3600  # seconds.
