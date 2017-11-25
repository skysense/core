import argparse
import os
from collections import deque
from time import time

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.contrib.rnn.python.ops.rnn_cell import PhasedLSTMCell

from model.model_helpers import stacked_lstm, ModelFileLogger, compute_returns


def get_batch(bs, prices, sequence_length):
    batch_x = []
    batch_t = []
    batch_y = []
    for jj in range(bs):
        start = np.random.choice(range(len(prices) - sequence_length - 1))
        values = prices[start: start + sequence_length + 1].values
        x = np.array(values[0:-1, 1], dtype=float)
        y = np.array(values[-1, 1], dtype=float)
        t = np.array(values[0:-1, 0], dtype=float)
        batch_x.append(x)
        batch_t.append(t)
        batch_y.append(y)
    return np.expand_dims(batch_x, axis=2), np.expand_dims(batch_t, axis=2), np.expand_dims(batch_y, axis=1)


def run_training(lstm_cell, hidden_size, batch_size, steps, log_file=None):
    if log_file is None:
        log_file = os.path.join('log', 'log.tsv')

    # MODEL PART #######################
    sequence_length = 20  # for now let's do like this.
    learning_rate = 1e-7
    print(hidden_size)
    print(batch_size)
    print(steps)
    print(learning_rate)
    print(sequence_length)

    file_logger = ModelFileLogger(log_file,
                                  ['step', 'testing_loss', 'benchmark_loss', 'running_difference', 'running_acc'])
    x_ = tf.placeholder(tf.float32, (batch_size, sequence_length, 1))
    t_ = tf.placeholder(tf.float32, (batch_size, sequence_length, 1))
    y_ = tf.placeholder(tf.float32, (batch_size, 1))

    inputs = (t_, x_)

    rnn_out = stacked_lstm(cell_fn=lstm_cell,
                           input_tensor=inputs,
                           num_cells=hidden_size,
                           num_lstm_layers=3,
                           return_only_last_output=True)

    out = slim.fully_connected(inputs=rnn_out,
                               num_outputs=hidden_size,
                               activation_fn=tf.nn.tanh)

    out = slim.fully_connected(inputs=out,
                               num_outputs=1,
                               activation_fn=None)

    print('*' * 80)
    print('TRAINABLE VARIABLES')
    for tv in tf.trainable_variables():
        print(tv)
    num_params = np.sum([np.prod([int(e) for e in d.shape.dims], axis=0) for d in tf.trainable_variables()])
    print('TOTAL NUMBER OF TRAINABLE VARIABLES = {}'.format(num_params))
    print('*' * 80)

    loss = 100 * tf.reduce_mean(tf.abs(out - y_))
    benchmark_loss = 100 * tf.reduce_mean(tf.abs(y_))
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)  # clip please.

    sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
    sess.run(tf.global_variables_initializer())

    # DATA PART #######################
    # removing the columns where the last price did not move. It biases the model.
    prices = pd.read_csv(os.path.join('data_examples', 'btc_price_2017-09-13T03:45:28+00:00.csv'))
    prices = prices[['timestamp', 'last']].astype(np.float)
    prices['last'] = compute_returns(prices['last'])
    prices = prices[prices['last'] != 0]

    # RUN PART #######################
    running_difference = deque(maxlen=100)
    running_accuracy = deque(maxlen=100)
    for i in range(steps):
        x_train, t_train, y_train = get_batch(batch_size, prices, sequence_length)
        st = time()
        sess.run([train_step], feed_dict={x_: x_train, y_: y_train, t_: t_train})  # gradient update.

        x_test, t_test, y_test = get_batch(batch_size, prices, sequence_length)
        te_loss, be_loss = sess.run([loss, benchmark_loss],
                                    feed_dict={x_: x_test, y_: y_test, t_: t_test})
        running_difference.append(be_loss - te_loss)
        running_accuracy.append(te_loss < be_loss)
        print(
            'steps = {0} | time {1:.3f} | te_loss = {2:.6f}, be_loss = {3:.6f}, r_diff = {4:.6f}, r_acc = {5:.3f}'.format(
                str(i).zfill(6), time() - st, te_loss, be_loss, np.mean(running_difference), np.mean(running_accuracy)))
        file_logger.write([i, te_loss, be_loss, np.mean(running_difference), np.mean(running_accuracy)])

    file_logger.close()


def main():
    model_class, log_file = get_parameters()
    run_training(lstm_cell=model_class, hidden_size=1024, batch_size=32, steps=10000, log_file=log_file)


def get_parameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model')  # BasicLSTMCell, PhasedLSTMCell
    parser.add_argument('-g', '--log_file')
    args = parser.parse_args()
    model_str = args.model
    log_file = args.log_file
    if model_str is None:
        model = PhasedLSTMCell
    else:
        model = globals()[model_str]
    print('Using model = {}'.format(model))
    return model, log_file


if __name__ == '__main__':
    main()
