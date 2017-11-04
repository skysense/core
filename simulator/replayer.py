import pandas as pd


class Replayer:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = pd.read_csv(self.data_file, index_col=0, parse_dates=True).to_dict(orient='records')
        self.cursor = 0

    def reset(self):
        self.cursor = 0

    def next(self):
        d = self.data[self.cursor]
        self.cursor += 1
        return d


"""
Format is:
{'high': '3217.17',
 'last': '3094.11',
 'timestamp': '1506249009',
 'bid': '3087.69',
 'vwap': '3149.80',
 'volume': '1148.62901405',
 'low': '3050.50',
 'ask': '3094.11',
 'open': '3174.97'}
"""
