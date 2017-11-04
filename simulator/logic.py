# will contain=
# - re player for bid-ask prices.
# - basic in memory logic database and so on
from _pydecimal import Decimal
from datetime import datetime
from random import randint

from flask import request

BTC_EUR_FIXED_PRICE = 6000

INITIAL_EUR_CASH_AMOUNT = 1000

FMT_DATETIME = '%Y-%m-%d %H:%M:%S'


def generate_random_transaction_id():
    return str(randint(a=10000000, b=99999999))


def generate_random_order_id():
    return str(randint(a=100000000, b=999999999))


def resting_order(user, is_buy=True):
    if request.method == 'POST':
        data = request.form
        order_id = generate_random_order_id()
        user.open_orders[order_id] = {'price': Decimal(str(BTC_EUR_FIXED_PRICE)),
                                      'currency_pair': 'BTC/EUR',
                                      'datetime': str(datetime.now().strftime(FMT_DATETIME)),
                                      'amount': Decimal(data['amount']),
                                      'type': '0' if is_buy else '1',  # BUY
                                      'id': str(order_id)
                                      }
        return 'Order is resting.'
    else:
        return 'Only available through POST.'


def send_order(user, is_buy=True):
    if request.method == 'POST':
        data = request.form
        print(data)
        if int(data['admin_resting_order']):
            return resting_order(user, is_buy)
        else:
            return market_order(user, is_buy)
    else:
        return 'Only available through POST.'


def market_order(user, is_buy=True):
    # https://www.bitstamp.net/api/v2/buy/market/btceur/
    # {'amount': 0.003, 'key': '***', 'signature': '***', 'nonce': '1506251375795815'}
    if request.method == 'POST':
        data = request.form
        print(data)
        btc_order_amount = float(data['amount'])
        total_price_eur = btc_order_amount * BTC_EUR_FIXED_PRICE

        if is_buy:
            if user.eur_balance < total_price_eur:
                return str({'status': 'error', 'reason': {
                    '__all__': ['You can only buy {0} EUR. '
                                'Check your account balance '
                                'for details.'.format(user.eur_balance)]}})

            user.btc_available += btc_order_amount
            user.btc_balance += btc_order_amount
            user.eur_available -= total_price_eur
            user.eur_balance -= total_price_eur
        else:

            if user.btc_balance < btc_order_amount:
                return str({'status': 'error', 'reason': {
                    '__all__': ['You can only sell {0} BTC. '
                                'Check your account balance '
                                'for details.'.format(user.btc_balance)]}})

            user.btc_available -= btc_order_amount
            user.btc_balance -= btc_order_amount
            user.eur_available += total_price_eur
            user.eur_balance += total_price_eur

        total_fees = user.btceur_fee * 0.01 * total_price_eur
        user.eur_available -= total_fees
        user.eur_balance -= total_fees

        order_id = generate_random_order_id()
        transaction_id = generate_random_transaction_id()

        btc_order_amount_str = str(btc_order_amount) if is_buy else str(-btc_order_amount)
        fiat_total = str(total_price_eur) if is_buy else str(-total_price_eur)
        date = str(datetime.now().strftime(FMT_DATETIME))
        user.transactions.append(
            {'fee': str(total_fees),
             'order_id': order_id,
             'datetime': date,
             'usd': 0.0,
             'btc': btc_order_amount_str,
             'btc_eur': BTC_EUR_FIXED_PRICE,
             'type': '2',
             'id': transaction_id,
             'eur': fiat_total
             })

        user.order_statuses[order_id] = \
            {'status': 'Finished',
             'transactions': [
                 {'fee': str(total_fees),
                  'price': str(BTC_EUR_FIXED_PRICE),
                  'datetime': date,
                  'btc': btc_order_amount_str,
                  'tid': transaction_id,
                  'type': '2',  # MARKET TRADE
                  'eur': fiat_total
                  }
             ]}
        return 'Order sent.'
    else:
        return 'Only available through POST.'


class UserAccount:
    def __init__(self):
        self.btc_available = 0.00000000
        self.btc_balance = 0.00000000

        self.btc_reserved = 0.00000000
        self.btceur_fee = 0.25
        self.btcusd_fee = 0.25

        self.eth_available = 0.00000000
        self.eth_balance = 0.00000000
        self.eth_reserved = 0.00000000
        self.ethbtc_fee = 0.25
        self.etheur_fee = 0.25

        self.ethusd_fee = 0.00
        self.eur_available = INITIAL_EUR_CASH_AMOUNT

        self.eur_balance = INITIAL_EUR_CASH_AMOUNT
        self.eur_reserved = 0.00

        self.eurusd_fee = 0.25
        self.ltc_available = 0.00000000
        self.ltc_balance = 0.00000000

        self.ltc_reserved = 0.00000000
        self.ltcbtc_fee = 0.25

        self.ltceur_fee = 0.25
        self.ltcusd_fee = 0.25

        self.usd_available = 0.00
        self.usd_balance = 0.00

        self.usd_reserved = 0.00
        self.xrp_available = 0.00000000

        self.xrp_balance = 0.00000000
        self.xrp_reserved = 0.00000000

        self.xrpbtc_fee = 0.25
        self.xrpeur_fee = 0.25
        self.xrpusd_fee = 0.25

        # first transaction is the payment.
        self.transactions = [
            {'fee': '0.00',
             'btc_usd': '0.00',
             'datetime': str(datetime.now().strftime(FMT_DATETIME)),
             'usd': 0.0,
             'btc': 0.0,
             'type': '0',
             'id': 22034181,
             'eur': str(INITIAL_EUR_CASH_AMOUNT)}]

        self.open_orders = []

        self.order_statuses = {}

    def balance(self):
        return {'btc_available': self.btc_available,
                'btc_balance': self.btc_balance,
                'btc_reserved': self.btc_reserved,
                'btceur_fee': self.btceur_fee,
                'btcusd_fee': self.btcusd_fee,
                'eth_available': self.eth_available,
                'eth_balance': self.eth_balance,
                'eth_reserved': self.eth_reserved,
                'ethbtc_fee': self.ethbtc_fee,
                'etheur_fee': self.etheur_fee,
                'ethusd_fee': self.ethusd_fee,
                'eur_available': self.eur_available,
                'eur_balance': self.eur_balance,
                'eur_reserved': self.eur_reserved,
                'eurusd_fee': self.eurusd_fee,
                'ltc_available': self.ltc_available,
                'ltc_balance': self.ltc_balance,
                'ltc_reserved': self.ltc_reserved,
                'ltcbtc_fee': self.ltcbtc_fee,
                'ltceur_fee': self.ltceur_fee,
                'ltcusd_fee': self.ltcusd_fee,
                'usd_available': self.usd_available,
                'usd_balance': self.usd_balance,
                'usd_reserved': self.usd_reserved,
                'xrp_available': self.xrp_available,
                'xrp_balance': self.xrp_balance,
                'xrp_reserved': self.xrp_reserved,
                'xrpbtc_fee': self.xrpbtc_fee,
                'xrpeur_fee': self.xrpeur_fee,
                'xrpusd_fee': self.xrpusd_fee}
