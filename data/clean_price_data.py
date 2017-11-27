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
    arg_p.add_argument('--data_dir', type=str, default='bitstamp_record_price')
    arg_p.add_argument('--output_file', type=str, default='price.csv')
    return arg_p


HEADERS = ['high', 'last', 'timestamp', 'bid', 'vwap', 'volume', 'low', 'ask', 'open']

np.set_printoptions(threshold=np.nan)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def clean_data(data_dir, output_file):
    np_data = []
    all_json = glob(data_dir + '/*.json')
    print('Found {} prices updates.'.format(len(all_json)))
    for filename in tqdm(natsorted(all_json)):
        # print(filename)
        try:
            with open(filename, 'r') as r:
                d = json.load(r)
                l = []
                for header in HEADERS:
                    l.append(str(d[header]))
            np_data.append(l)
        except:
            print('Problem with filename [{}].'.format(filename))

    if len(np_data) == 0:
        d = pd.read_csv('./data_examples/btc_price_2017-09-13T03:45:28+00:00.csv')
        print('No data available in {}'.format(data_dir))
        print('Using Data Examples')
        return d
        # raise Exception('No data available in {}'.format(data_dir))

    np_data = np.array(np_data)
    d = pd.DataFrame(np_data, index=np_data[:, 2])
    d.columns = HEADERS
    d.index = d.index.map(lambda ts: datetime.datetime.fromtimestamp(int(ts)))
    print('Data set has {} rows.'.format(len(d)))
    d.drop_duplicates(inplace=True)
    print('Removing duplicates...')
    print('Data set has {} rows.'.format(len(d)))
    d.index.names = ['DateTime_UTC']
    d.to_csv(output_file)
    print(d)
    return d


def run(arg_p):
    clean_data(arg_p.data_dir, arg_p.output_file)


if __name__ == '__main__':
    run(arg_parse().parse_args(sys.argv[1:]))
