import sys
from argparse import ArgumentParser

import matplotlib.pyplot as plt
import pandas as pd


def arg_parse():
    arg_p = ArgumentParser()
    arg_p.add_argument('--balance_file', type=str)  # in log/
    return arg_p


def run(balance_file):
    df = pd.read_csv(balance_file, sep='|')
    df.rename(columns=lambda x: x.strip(), inplace=True)
    # df = df.apply(lambda x: x.str.strip())
    print(df.head())
    plt.figure(1)
    plt.subplot(1, 2, 1)
    df['btc_balance'].plot(title='BTC Balance')  # no need to specify for first axis
    plt.subplot(1, 2, 2)
    df['eur_available'].plot(ax=plt.gca(), title='EUR Balance')
    plt.show()


if __name__ == '__main__':
    run(arg_parse().parse_args(sys.argv[1:]).balance_file)
