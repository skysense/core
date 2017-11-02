import datetime
import json
import sys
from argparse import ArgumentParser
from glob import glob

import numpy as np
import pandas as pd
from natsort import natsorted
from tqdm import tqdm


def arg_parse():
    arg_p = ArgumentParser()
    arg_p.add_argument('--data_dir', type=str, default='bitstamp_record_order_book')
    arg_p.add_argument('--output_file', type=str, default='order_book.csv')
    arg_p.add_argument('--order_book_desired_depth', type=int, default=3)
    return arg_p


def generate_header(order_book_depth):
    headers = ['timestamp']
    for i in range(order_book_depth):
        headers.append('bid_price_level_{}'.format(i))
        headers.append('bid_qty_level_{}'.format(i))
        headers.append('ask_price_level_{}'.format(i))
        headers.append('ask_qty_level_{}'.format(i))
    return headers


np.set_printoptions(threshold=np.nan)
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class OrderBookDepthExceeded(Exception):
    def __init__(self, max_depth):
        self.max_depth = max_depth


def process_single_order_book_update(d, order_book_depth):
    # result['asks'] => List of <class 'list'>: ['3493.97', '1.97871436'], [...]
    # result['bids'] => '1502437832'
    # result['timestamp'] => <class 'list'>: ['3484.76', '1.65170000'], [...]
    l = [d['timestamp']]
    for depth, (bid, ask) in enumerate(zip(d['bids'], d['asks'])):
        if depth >= order_book_depth:
            break
        bid_price_level, bid_qty_level = bid
        ask_price_level, ask_qty_level = ask
        l.append(bid_price_level)
        l.append(bid_qty_level)
        l.append(ask_price_level)
        l.append(ask_qty_level)
    cur_depth = int((len(l) - 1) / 4)
    if order_book_depth > cur_depth:
        raise OrderBookDepthExceeded(cur_depth)
    return l


def read(arg_p):
    headers = generate_header(arg_p.order_book_desired_depth)
    data_dir = arg_p.data_dir
    np_data = []
    all_json = glob(data_dir + '/*.json')
    print('Found {} order book updates.'.format(len(all_json)))
    for filename in tqdm(natsorted(all_json)):
        try:
            with open(filename, 'r') as r:
                d = json.load(r)
                l = process_single_order_book_update(d, arg_p.order_book_desired_depth)
            assert len(l) == len(headers)
            np_data.append(l)
        except OrderBookDepthExceeded as depth_excedeed_exc:
            print('================= Max depth is {} ================= '.format(depth_excedeed_exc.max_depth))
            print('================= Program will exit ================='.format(depth_excedeed_exc.max_depth))
            exit(-1)
        except:
            print('Problem with filename [{}].'.format(filename))

    if len(np_data) == 0:
        raise Exception('No data available in {}'.format(data_dir))

    np_data = np.array(np_data)
    d = pd.DataFrame(np_data, index=np_data[:, 0])
    d.columns = headers
    d.index = d.index.map(lambda ts: datetime.datetime.fromtimestamp(int(ts)))
    print('Data set has {} rows.'.format(len(d)))
    d.drop_duplicates(inplace=True)
    print('Removing duplicates...')
    print('Data set has {} rows.'.format(len(d)))
    d.index.names = ['DateTime_UTC']
    d.to_csv(arg_p.output_file)
    print(d)
    return d


if __name__ == '__main__':
    read(arg_parse().parse_args(sys.argv[1:]))
