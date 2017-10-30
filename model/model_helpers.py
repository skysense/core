import tensorflow as tf
from tensorflow.python.ops.rnn import dynamic_rnn


def multi_lstm(cell_fn, input_tensor, num_cells, num_lstm_layers=1, return_only_last_output=True):
    (x, t) = input_tensor
    for i in range(num_lstm_layers):
        x, _ = dynamic_rnn(cell=cell_fn(num_cells), inputs=(x, t), dtype=tf.float32, scope='LSTM_' + str(i))
    if return_only_last_output == True:
        return tf.squeeze(x[:, -1, :])
    return x
