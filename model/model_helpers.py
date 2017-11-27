import numpy as np
import tensorflow as tf
from tensorflow.python.ops.rnn import dynamic_rnn


def stacked_lstm(cell_fn, input_tensor, num_cells, num_lstm_layers=1, return_only_last_output=True):
    (x, t) = input_tensor
    for i in range(num_lstm_layers):
        x, _ = dynamic_rnn(cell=cell_fn(num_cells), inputs=(x, t), dtype=tf.float32, scope='LSTM_' + str(i))
    if return_only_last_output:
        return tf.squeeze(x[:, -1, :])
    return x


def split_prices(prices, ratio=np.array([0.7, 0.2, 0.1])):
    n = prices.shape[0]
    n_train = int(np.floor(n * ratio[0]))
    n_cv = int(np.floor(n * ratio[1]))
    prices_train = prices.iloc[:n_train, :]
    prices_cv = prices.iloc[n_train:n_train + n_cv, :]
    prices_test = prices.iloc[n_train + n_cv:, :]
    return prices_train, prices_cv, prices_test


def get_batch(batch_size, prices, sequence_length):
    batch_x = []
    batch_t = []
    batch_y = []
    for jj in range(batch_size):
        start = np.random.choice(range(len(prices) - sequence_length - 1))
        values = prices[start: start + sequence_length + 1].values
        x = np.array(values[0:-1, 1], dtype=float)
        y = np.array(values[-1, 1], dtype=float)
        t = np.array(values[0:-1, 0], dtype=float)
        batch_x.append(x)
        batch_t.append(t)
        batch_y.append(y)
    return np.expand_dims(batch_x, axis=2), np.expand_dims(batch_t, axis=2), np.expand_dims(batch_y, axis=1)


class ModelFileLogger:
    def __init__(self, full_filename, headers):
        self._headers = headers
        self._out_fp = open(full_filename, 'w')
        self._write(headers)

    def write(self, line):
        assert len(line) == len(self._headers)
        self._write(line)

    def close(self):
        self._out_fp.close()

    def _write(self, arr):
        arr = [str(e) for e in arr]
        self._out_fp.write(' '.join(arr) + '\n')
        self._out_fp.flush()


class ModelOutput:
    def __init__(self, buy_confidence, sell_confidence, hold_confidence):
        self.buy_confidence = float(buy_confidence)
        self.sell_confidence = float(sell_confidence)
        self.hold_confidence = float(hold_confidence)
        if np.abs(self.buy_confidence + self.sell_confidence + self.hold_confidence - 1) > 1e-5:
            raise Exception('buy, sell and hold confidence do not add up to 1.')

    def __str__(self):
        return '[buy_confidence = {0:.3f}, ' \
               'sell_confidence = {1:.3f}, ' \
               'hold_confidence = {2:.3f}]'.format(self.buy_confidence,
                                                   self.sell_confidence,
                                                   self.hold_confidence)
