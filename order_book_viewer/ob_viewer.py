import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from natsort import natsorted

# ORDER_BOOK_FILENAME = '../data_examples/ob_btc_price_12_15_2017/ob_btc_price_12_15_2017-12:36:28.csv'
ORDER_BOOK_FILENAME = '../data_examples/ob_btc_price_12_15_2017/ob.csv'

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 100000)


def view():
    if not os.path.isfile(ORDER_BOOK_FILENAME):
        print('Could not find the order book filename.')
    ob = pd.read_csv(ORDER_BOOK_FILENAME)

    price_columns = natsorted(list(filter(lambda x: 'price' in x, list(ob.columns))))
    bid_price_columns = natsorted(list(filter(lambda x: 'bid' in x, list(price_columns))), reverse=True)
    ask_price_columns = list(filter(lambda x: 'ask' in x, list(price_columns)))

    qty_columns = natsorted(list(filter(lambda x: 'qty' in x, list(ob.columns))))
    bid_qty_columns = list(filter(lambda x: 'bid' in x, list(qty_columns)))
    ask_qty_columns = list(filter(lambda x: 'ask' in x, list(qty_columns)))

    # ob[bid_price_columns]
    # ob[ask_price_columns]

    # ob[bid_qty_columns] = ob[bid_qty_columns].cumsum(axis=1)
    # ob[ask_qty_columns] = ob[ask_qty_columns].cumsum(axis=1)

    bid_qty_columns = natsorted(bid_qty_columns, reverse=True)
    bid_price_columns = natsorted(bid_price_columns, reverse=True)

    all_qty_columns = bid_qty_columns + ask_qty_columns
    all_price_columns = bid_price_columns + ask_price_columns

    print(all_qty_columns)
    print(all_price_columns)

    qty = ob[all_qty_columns]

    prices = ob[all_price_columns]

    plt.ion()
    axes = plt.gca()

    date_times = ob['DateTime_UTC'].values
    for i in range(10000):
        current_price = prices[i:i + 1].values.flatten()
        current_quantity = qty[i:i + 1].values.flatten()
        bid_sum_qty = '{0:.2f}'.format(np.sum(current_quantity[:20]))
        ask_sum_qty = '{0:.2f}'.format(np.sum(current_quantity[20:]))
        plt.title(date_times[i] + ' - BID: {0} / ASK: {1}'.format(bid_sum_qty, ask_sum_qty))
        axes.bar(current_price, current_quantity, color=['lime'] * 20 + ['red'] * 20)
        # plt.bar(current_price, current_quantity, color=['lime'] * 20 + ['red'] * 20)
        plt.draw()
        plt.pause(0.00001)
        plt.cla()
    plt.show()


if __name__ == '__main__':
    view()
