import datetime
import json
from glob import glob

import numpy as np
import pandas as pd
from natsort import natsorted

DATA_DIR = '/tmp/out/out/'

HEADERS = ['high', 'last', 'timestamp', 'bid', 'vwap', 'volume', 'low', 'ask', 'open']

np.set_printoptions(threshold=np.nan)
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def read():
    data = []
    for filename in natsorted(glob(DATA_DIR + '*.json')):
        print(filename)
        try:
            with open(filename, 'r') as r:
                d = json.load(r)
                l = []
                for header in HEADERS:
                    l.append(str(d[header]))
            data.append(l)
        except:
            print('Problem with filename [{}].'.format(filename))

    if len(data) == 0:
        raise Exception('No data available in {}'.format(DATA_DIR))

    data = np.array(data)
    ret = pd.DataFrame(data, index=data[:, 2])
    ret.columns = HEADERS
    ret.index = ret.index.map(lambda ts: datetime.datetime.fromtimestamp(int(ts)))
    ret.drop_duplicates(inplace=True)
    ret.index.names = ['DateTime_UTC']
    print(ret)
    return ret


if __name__ == '__main__':
    read()
