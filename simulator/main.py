import datetime
from decimal import Decimal

from flask import Flask, url_for
from flask import request

from connectivity.calls import DEFAULT_CURRENCY_PAIR
from simulator import logic

app = Flask(__name__)
user = logic.UserAccount()

BTC_EUR_FIXED_PRICE = 3000


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/', methods=['GET', 'POST'])
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
            # links is now a list of url, endpoint tuples
    return '<br/>'.join(sorted(['<a href="{0}">{0}</a> -> {1}()'.format(l, v) for (l, v) in links]))


@app.route('/balance/', methods=['GET', 'POST'])
def balance():
    # {'btc_available': '0.00300000', 'btc_balance': '0.00300000',
    # 'btc_reserved': '0.00000000', 'btceur_fee': '0.25', 'btcusd_fee': '0.25',
    # 'eth_available': '0.00000000', 'eth_balance': '0.00000000', 'eth_reserved':
    # '0.00000000', 'ethbtc_fee': '0.00', 'etheur_fee': '0.00',
    # 'ethusd_fee': '0.00', 'eur_available': '95.72',
    # 'eur_balance': '95.72', 'eur_reserved': '0.00',
    # 'eurusd_fee': '0.25', 'ltc_available':
    # '0.00000000', 'ltc_balance': '0.00000000',
    # 'ltc_reserved': '0.00000000', 'ltcbtc_fee': '0.25',
    # 'ltceur_fee': '0.25', 'ltcusd_fee': '0.25',
    # 'usd_available': '0.00', 'usd_balance': '0.00',
    # 'usd_reserved': '0.00', 'xrp_available': '0.00000000',
    # 'xrp_balance': '0.00000000', 'xrp_reserved': '0.00000000',
    # 'xrpbtc_fee': '0.25', 'xrpeur_fee': '0.25', 'xrpusd_fee': '0.25'}
    return 'Hello World!'


# curl -X POST http://127.0.0.1:5000/buy/btceur/ -d "{'amount': 0.003, 'key': '***', 'signature': '***', 'nonce': '1506251375795815'}"
@app.route('/buy/{}/'.format(DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'])
def buy():
    if request.method == 'POST':
        data = request.form
        print(data)
        if int(data['admin_resting_order']):
            print('Order is resting.')
            order_id = 320422620
            user.open_orders[order_id] = {'price': Decimal(str(BTC_EUR_FIXED_PRICE)),
                                          'currency_pair': 'BTC/EUR',
                                          'datetime': datetime.datetime(2017, 9, 24, 10, 50, 50),
                                          'amount': Decimal(data['amount']),
                                          'type': '0',  # BUY
                                          'id': str(order_id)}
        else:
            buy_market()


@app.route('/sell/{}/'.format(DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        data = request.form
        print(data)
        if int(data['admin_resting_order']):
            print('Order is resting.')
            order_id = 320422620
            user.open_orders[order_id] = {'price': Decimal(str(BTC_EUR_FIXED_PRICE)),
                                          'currency_pair': 'BTC/EUR',
                                          'datetime': datetime.datetime(2017, 9, 24, 10, 50, 50),
                                          'amount': Decimal(data['amount']),
                                          'type': '1',  # SELL
                                          'id': str(order_id)}
        else:
            sell_market()


@app.route('/buy/market/{}/'.format(DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'])
def buy_market():
    # https://www.bitstamp.net/api/v2/buy/market/btceur/
    # {'amount': 0.003, 'key': '***', 'signature': '***', 'nonce': '1506251375795815'}
    if request.method == 'POST':
        data = request.form
        print(data)
        btc_order_amount = float(data['amount'])

        total_price_eur = btc_order_amount * BTC_EUR_FIXED_PRICE

        user.btc_available += btc_order_amount
        user.btc_balance += btc_order_amount

        user.eur_available -= total_price_eur
        user.eur_balance -= total_price_eur

        total_fees = user.btceur_fee * total_price_eur
        user.eur_available -= total_fees
        user.eur_balance -= total_fees

        order_id = 320464858
        transaction_id = 22155667

        user.transactions.append(
            {'fee': str(total_fees),
             'order_id': order_id,
             'datetime': '2017-09-24 11:09:39',
             'usd': 0.0,
             'btc': str(btc_order_amount),
             'btc_eur': BTC_EUR_FIXED_PRICE,
             'type': '2',
             'id': transaction_id,
             'eur': str(-total_price_eur)})

        user.order_statuses[order_id] = {'status': 'Finished', 'transactions': [
            {'fee': str(total_fees),
             'price': str(BTC_EUR_FIXED_PRICE),
             'datetime': '2017-09-24 11:09:39',
             'btc': '0.00300000',
             'tid': transaction_id,
             'type': 2,  # MARKET TRADE
             'eur': str(total_price_eur)}]}

    return 'Buy'


@app.route('/sell/market/{}/'.format(DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'])
def sell_market():
    if request.method == 'POST':
        data = request.form
        print(data)
        btc_order_amount = float(data['amount'])

        total_price_eur = btc_order_amount * BTC_EUR_FIXED_PRICE

        user.btc_available -= btc_order_amount
        user.btc_balance -= btc_order_amount

        user.eur_available += total_price_eur
        user.eur_balance += total_price_eur

        total_fees = user.btceur_fee * total_price_eur
        user.eur_balance -= total_fees
        user.eur_balance -= total_fees

        order_id = 22155667
        transaction_id = 22155667

        user.transactions.append(
            {'fee': str(total_fees),
             'order_id': order_id,
             'datetime': '2017-09-24 11:09:39',
             'usd': 0.0,
             'btc': str(-btc_order_amount),
             'btc_eur': BTC_EUR_FIXED_PRICE,
             'type': '2',
             'id': transaction_id,
             'eur': str(total_price_eur)})

        user.order_statuses[order_id] = {'status': 'Finished', 'transactions': [
            {'fee': str(total_fees),
             'price': str(BTC_EUR_FIXED_PRICE),
             'datetime': '2017-09-24 11:09:39',
             'btc': '0.00300000',
             'tid': transaction_id,
             'type': 2,  # MARKET TRADE
             'eur': str(total_price_eur)}]}

    return 'Sell'


@app.route('/cancel_order/', methods=['GET', 'POST'])
def cancel_order():
    if request.method == 'POST':
        data = request.form
        print(data)
        order_id = data['id']
        del user.open_orders[order_id]
    return 'Hello World!'


# {'id': '320464858', 'key': '***', 'signature': '***', 'nonce': '1506251383558164'}
@app.route('/order_status/', methods=['GET', 'POST'])
def order_status():
    if request.method == 'POST':
        data = request.form
        print(data)
        order_id = data['id']
        return user.order_statuses[order_id]


@app.route('/open_orders/all/', methods=['GET', 'POST'])
def open_orders_all():
    return NotImplementedError()


@app.route('/transactions/{}/'.format(DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'])
def transactions():
    raise NotImplementedError()


@app.route('/user_transactions/', methods=['GET', 'POST'])
def user_transactions():
    return user.transactions[::-1]


if __name__ == '__main__':
    app.run()
