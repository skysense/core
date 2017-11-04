from . import calls
from constants import API_URL_V1
from constants import API_URL_V2

# Constants
BUY_LIMIT_ORDER_TYPE_BUY = 0
BUY_LIMIT_ORDER_TYPE_SELL = 1

OPEN_ORDERS_TYPE_BUY = 0
OPEN_ORDERS_TYPE_SELL = 1

SELL_LIMIT_ORDER_TYPE_BUY = 0
SELL_LIMIT_ORDER_TYPE_SELL = 1

TRANSACTIONS_SORT_ASCENDING = 'asc'
TRANSACTIONS_SORT_DESCENDING = 'desc'

USER_TRANSACTIONS_SORT_ASCENDING = 'asc'
USER_TRANSACTIONS_SORT_DESCENDING = 'desc'

USER_TRANSACTIONS_TYPE_DEPOSIT = 0
USER_TRANSACTIONS_TYPE_WITHDRAWAL = 1
USER_TRANSACTIONS_TYPE_MARKET_TRADE = 2

WITHDRAWAL_REQUEST_TYPE_SEPA = 0
WITHDRAWAL_REQUEST_TYPE_BITCOIN = 1
WITHDRAWAL_REQUEST_TYPE_WIRE = 2
WITHDRAWAL_REQUEST_TYPE_BITSTAMP_CODE_1 = 3
WITHDRAWAL_REQUEST_TYPE_BITSTAMP_CODE_2 = 4
WITHDRAWAL_REQUEST_TYPE_MTGOX = 5

WITHDRAWAL_REQUEST_STATUS_OPEN = 0
WITHDRAWAL_REQUEST_STATUS_IN_PROCESS = 1
WITHDRAWAL_REQUEST_STATUS_FINISHED = 2
WITHDRAWAL_REQUEST_STATUS_CANCELLED = 3
WITHDRAWAL_REQUEST_STATUS_FAILED = 4

# API_URL_V1 = 'https://www.bitstamp.net/api/'
# API_URL_V2 = 'https://www.bitstamp.net/api/v2/'

# API_URL_V1 = 'http://127.0.0.1:5000/'
# API_URL_V2 = 'http://127.0.0.1:5000/v2/'

# Wrapper functions

def account_balance(client_id, api_key, api_secret):
    return (
        calls.APIAccountBalanceCall(client_id, api_key, api_secret).call(API_URL_V2)
    )


def bitcoin_deposit_address(client_id, api_key, api_secret):
    return (
        calls.APIBitcoinDepositAddressCall(client_id, api_key, api_secret).call(API_URL_V1)
    )


def bitcoin_withdrawal(client_id, api_key, api_secret, amount, address):
    return (
        calls.APIBitcoinWithdrawalCall(client_id, api_key, api_secret).call(API_URL_V1, amount=amount, address=address)
    )


def buy_limit_order(client_id, api_key, api_secret, amount, price):
    return (
        calls.APIBuyLimitOrderBTCEURCall(client_id, api_key, api_secret).call(API_URL_V2, amount=amount, price=price)
    )


def cancel_order(client_id, api_key, api_secret, order_id):
    return (
        calls.APICancelOrderCall(client_id, api_key, api_secret).call(API_URL_V2, id=order_id)
    )


def order_status(client_id, api_key, api_secret, order_id):
    return (
        calls.APIOrderStatusCall(client_id, api_key, api_secret).call(API_URL_V1, id=order_id)
    )


def eur_usd_conversion_rate():
    return calls.APIEURUSDConversionRateCall().call(API_URL_V1)


def open_orders(client_id, api_key, api_secret):
    return (
        calls.APIOpenOrdersCall(client_id, api_key, api_secret).call(API_URL_V2)
    )


def order_book(group=True):
    return calls.APIOrderBookCall().call(API_URL_V2, group='1' if group else '0')


def ripple_deposit_address(client_id, api_key, api_secret):
    return (
        calls.APIRippleDepositAddressCall(client_id, api_key, api_secret).call(API_URL_V1)
    )


def ripple_withdrawal(
        client_id, api_key, api_secret, amount, address, currency):
    return (
        calls.APIRippleWithdrawalCall(client_id, api_key, api_secret).call(API_URL_V1)
    )


def sell_limit_order(client_id, api_key, api_secret, amount, price):
    return (
        calls.APISellLimitBTCEUROrderCall(client_id, api_key, api_secret).call(API_URL_V2, amount=amount, price=price)
    )


def ticker():
    return calls.APITickerCall().call(API_URL_V2)


def transactions(offset=0, limit=100, sort=TRANSACTIONS_SORT_DESCENDING):
    return calls.APITransactionsCall().call(API_URL_V2, offset=offset, limit=limit, sort=sort)


def unconfirmed_bitcoin_deposits(client_id, api_key, api_secret):
    return (
        calls.APIUnconfirmedBitcoinDepositsCall(client_id, api_key, api_secret).call(API_URL_V1)
    )


def user_transactions(
        client_id, api_key, api_secret, offset=0, limit=100,
        sort=USER_TRANSACTIONS_SORT_DESCENDING):
    return (
        calls.APIUserTransactionsCall(client_id, api_key, api_secret).call(API_URL_V2, offset=offset, limit=limit,
                                                                           sort=sort)
    )


def withdrawal_requests(client_id, api_key, api_secret):
    return (
        calls.APIWithdrawalRequestsCall(client_id, api_key, api_secret).call(API_URL_V1)
    )


def buy_market_order(client_id, api_key, api_secret, amount):
    return (
        calls.APIBuyMarketOrderBTCEURCall(client_id, api_key, api_secret).call(API_URL_V2, amount=amount)
    )


def sell_market_order(client_id, api_key, api_secret, amount):
    return (
        calls.APISellMarketOrderBTCEURCall(client_id, api_key, api_secret).call(API_URL_V2, amount=amount)
    )
