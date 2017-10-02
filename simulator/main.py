from flask import Flask, url_for

from connectivity.calls import DEFAULT_CURRENCY_PAIR

app = Flask(__name__)


# @app.route('/')
# def root():
#     return 'Hello World!'


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route('/')
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


@app.route('/balance/')
def balance():
    return 'Hello World!'


@app.route('/buy/{}/'.format(DEFAULT_CURRENCY_PAIR))
def buy():
    return 'Hello World!'


@app.route('/sell/{}/'.format(DEFAULT_CURRENCY_PAIR))
def sell():
    return 'Hello World!'


@app.route('/buy/market/{}/'.format(DEFAULT_CURRENCY_PAIR))
def buy_market():
    return 'Hello World!'


@app.route('/sell/market/{}/'.format(DEFAULT_CURRENCY_PAIR))
def sell_market():
    return 'Hello World!'


@app.route('/cancel_order/')
def cancel_order():
    return 'Hello World!'


@app.route('/order_status/')
def order_status():
    return 'Hello World!'


@app.route('/open_orders/all/')
def open_orders_all():
    return 'Hello World!'


@app.route('/transactions/{}/'.format(DEFAULT_CURRENCY_PAIR))
def transactions():
    return 'Hello World!'


@app.route('/user_transactions/')
def user_transactions():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
