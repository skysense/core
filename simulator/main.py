from flask import Flask, url_for
from flask import request

from constants import TRADING_DEFAULT_CURRENCY_PAIR
from simulator.logic import send_order, market_order, UserAccount

app = Flask(__name__)
user = UserAccount()


@app.route('/reset/', methods=['GET', 'POST'], strict_slashes=False)
def reset():
    global user
    user = UserAccount()
    return 'Reset.'


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def list_all_end_points():
    def has_no_empty_params(rule_):
        defaults = rule_.defaults if rule_.defaults is not None else ()
        arguments = rule_.arguments if rule_.arguments is not None else ()
        return len(defaults) >= len(arguments)

    links = []
    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return '<b>' + '<br/><br/>'.join(
        sorted(['<a href="{0}">{0}</a> -> {1}()'.format(l, v) for (l, v) in links])) + '</b>'


@app.route('/balance/', methods=['GET', 'POST'], strict_slashes=False)
def balance():
    return str(user.balance())
    # if request.method == 'GET':
    #     # for the web interface.
    #     return json.dumps(user.balance(), indent=4).replace('\n', '<br/>')
    # # post. returns a JSON.
    # return user.balance()


@app.route('/buy/{}/'.format(TRADING_DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'], strict_slashes=False)
def buy():
    return send_order(user, is_buy=True)


@app.route('/sell/{}/'.format(TRADING_DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'], strict_slashes=False)
def sell():
    return send_order(user, is_buy=False)


@app.route('/buy/market/{}/'.format(TRADING_DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'], strict_slashes=False)
def buy_market():
    return market_order(user, is_buy=True)


@app.route('/sell/market/{}/'.format(TRADING_DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'], strict_slashes=False)
def sell_market():
    return market_order(user, is_buy=False)


@app.route('/cancel_order/', methods=['GET', 'POST'], strict_slashes=False)
def cancel_order():
    if request.method == 'POST':
        data = request.form
        print(data)
        order_id = data['id']
        del user.open_orders[order_id]
        return 'Order canceled.'
    else:
        return 'Only available through POST.'


# {'id': '320464858', 'key': '***', 'signature': '***', 'nonce': '1506251383558164'}
@app.route('/order_status/', methods=['GET', 'POST'], strict_slashes=False)
def order_status():
    if request.method == 'POST':
        data = request.form
        print(data)
        order_id = data['id']
        return user.order_statuses[order_id]


@app.route('/open_orders/all/', methods=['GET', 'POST'], strict_slashes=False)
def open_orders_all():
    return user.open_orders


@app.route('/transactions/{}/'.format(TRADING_DEFAULT_CURRENCY_PAIR), methods=['GET', 'POST'], strict_slashes=False)
def transactions():
    raise user.transactions


@app.route('/user_transactions/', methods=['GET', 'POST'], strict_slashes=False)
def user_transactions():
    return user.transactions[::-1]


if __name__ == '__main__':
    """
    curl -X POST http://127.0.0.1:5000/buy/btceur/ -d "{'amount': 0.003, 'key': '***', 'signature': '***', 'nonce': '1506251375795815'}"
    curl -X POST http://127.0.0.1:5000/buy/market/btceur/ -d "amount=0.03&nounce=033"
    """
    app.run()

    # export PYTHONPATH=../:$PYTHONPATH; python3 main.py
