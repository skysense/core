import numpy as np
import pandas as pd

from helpers.utils import compute_returns

DATA_FILE = '../data_examples/btc_price_2017-09-13T03:45:28+00:00.csv'
DATA = pd.read_csv(DATA_FILE, sep=',', parse_dates=True, index_col=0)

np.set_printoptions(threshold=np.nan)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.4f}'.format


def run():
    d = pd.DataFrame(DATA[['timestamp', 'last']])
    d = d.head(10000)
    print(d)
    e = pd.DataFrame(d)
    print(len(e['last'].resample('5Min').ohlc().replace(np.nan, 0)))

    exit(1)

    d['returns'] = compute_returns(d['last'])
    print(d['returns'].head())

    print(d['returns'].rolling(window=2, center=False).mean().head())

    print(d['returns'])

    sr_column = 'sharpe_ratio_{}'.format(num_average_ticks)
    # is to make a forward apply not a backward apply as people usually do.
    d[sr_column] = pd.rolling_apply(d['returns'][::-1],
                                    window=num_average_ticks,
                                    func=sharpe_ratio,
                                    center=False).fillna(0)[::-1]

    print(d.tail(100))

    labels = ['SELL', 'HOLD', 'BUY']
    d['signals'] = pd.qcut(d[sr_column], q=[0, 0.05, 0.95, 1], labels=[0, 1, 2])

    print(d.head(100))
    print(d['signals'].head(100))
    d['signals'].astype(np.float).plot()
    import matplotlib.pyplot as plt
    plt.show()


if __name__ == '__main__':
    print(run())
