import logging

import numpy as np
import pandas as pd

np.set_printoptions(threshold=np.nan)
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class ModelDataRecorder:
    def __init__(self):
        self.HEADERS = ['high', 'last', 'timestamp', 'bid', 'vwap', 'volume', 'low', 'ask', 'open']
        self.np_data = []
        self.logger = logging.getLogger('ModelDataRecorder')

    def update(self, x):
        d = [x[header] for header in self.HEADERS]
        self.np_data.append(d)

    def get_data_frame(self):
        np_data = np.array(self.np_data)
        d = pd.DataFrame(np_data, index=np_data[:, 2], columns=self.HEADERS)
        d.index.names = ['DateTime_UTC']
        d.drop_duplicates(inplace=True)
        self.logger.info('Data set has {} rows.'.format(len(d)))
        return d
