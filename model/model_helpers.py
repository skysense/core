import tensorflow as tf
from tensorflow.python.ops.rnn import dynamic_rnn


def stacked_lstm(cell_fn, input_tensor, num_cells, num_lstm_layers=1, return_only_last_output=True):
    (x, t) = input_tensor
    for i in range(num_lstm_layers):
        x, _ = dynamic_rnn(cell=cell_fn(num_cells), inputs=(x, t), dtype=tf.float32, scope='LSTM_' + str(i))
    if return_only_last_output:
        return tf.squeeze(x[:, -1, :])
    return x


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
