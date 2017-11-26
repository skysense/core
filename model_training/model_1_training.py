import os
from collections import deque
from time import time

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.contrib.slim as slim
from tensorflow.contrib.rnn.python.ops.rnn_cell import PhasedLSTMCell

from helpers.utils import compute_returns
from model.model import Model
from model.model_helpers import stacked_lstm, ModelFileLogger


class Model1(Model):
    def __init__(self):
        super().__init__()
        self.log_file = os.path.join('log', 'log.tsv')
        self.hidden_size = 1024
        self.batch_size = 32
        self.steps = 10000

        self.sequence_length = 20  # for now let's do like this.
        self.learning_rate = 1e-7
        print(self.hidden_size)
        print(self.batch_size)
        print(self.steps)
        print(self.learning_rate)
        print(self.sequence_length)

        self.file_logger = ModelFileLogger(self.log_file,
                                           ['step', 'testing_loss', 'benchmark_loss',
                                            'running_difference', 'running_acc'])
        self.x_ = tf.placeholder(tf.float32, (self.batch_size, self.sequence_length, 1))
        self.t_ = tf.placeholder(tf.float32, (self.batch_size, self.sequence_length, 1))
        self.y_ = tf.placeholder(tf.float32, (self.batch_size, 1))

        inputs = (self.t_, self.x_)

        rnn_out = stacked_lstm(cell_fn=PhasedLSTMCell,
                               input_tensor=inputs,
                               num_cells=self.hidden_size,
                               num_lstm_layers=3,
                               return_only_last_output=True)

        out = slim.fully_connected(inputs=rnn_out,
                                   num_outputs=self.hidden_size,
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

        self.loss = 100 * tf.reduce_mean(tf.abs(out - self.y_))
        self.benchmark_loss = 100 * tf.reduce_mean(tf.abs(self.y_))
        self.train_step = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)  # clip please.

        self.sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
        self.sess.run(tf.global_variables_initializer())

    def get_batch(self, batch_size, prices, sequence_length):
        batch_x = []
        batch_t = []
        batch_y = []
        for jj in range(self.batch_size):
            start = np.random.choice(range(len(prices) - sequence_length - 1))
            values = prices[start: start + sequence_length + 1].values
            x = np.array(values[0:-1, 1], dtype=float)
            y = np.array(values[-1, 1], dtype=float)
            t = np.array(values[0:-1, 0], dtype=float)
            batch_x.append(x)
            batch_t.append(t)
            batch_y.append(y)
        return np.expand_dims(batch_x, axis=2), np.expand_dims(batch_t, axis=2), np.expand_dims(batch_y, axis=1)

    def train(self, replay_file=os.path.join('data_examples', 'btc_price_2017-09-13T03:45:28+00:00.csv')):
        # DATA PART #######################
        # removing the columns where the last price did not move. It biases the model.
        prices = pd.read_csv(replay_file, index_col=0, parse_dates=True)
        prices = prices[['last']].astype(np.float)
        prices['last'] = compute_returns(prices['last'])

        # RUN PART #######################
        running_difference = deque(maxlen=100)
        running_accuracy = deque(maxlen=100)
        for i in range(self.steps):
            x_train, t_train, y_train = self.get_batch(self.batch_size, prices, self.sequence_length)
            st = time()
            self.sess.run([self.train_step], feed_dict={self.x_: x_train,
                                                        self.y_: y_train,
                                                        self.t_: t_train})  # gradient update.

            x_test, t_test, y_test = self.get_batch(self.batch_size, prices, self.sequence_length)
            te_loss, be_loss = self.sess.run([self.loss, self.benchmark_loss],
                                             feed_dict={self.x_: x_test,
                                                        self.y_: y_test,
                                                        self.t_: t_test})
            running_difference.append(be_loss - te_loss)
            running_accuracy.append(te_loss < be_loss)
            print(
                'steps = {0} | time {1:.3f} | te_loss = {2:.6f}, be_loss = {3:.6f}, r_diff = {4:.6f}, r_acc = {5:.3f}'.format(
                    str(i).zfill(6), time() - st, te_loss, be_loss, np.mean(running_difference),
                    np.mean(running_accuracy)))
            self.file_logger.write([i, te_loss, be_loss, np.mean(running_difference), np.mean(running_accuracy)])

        self.file_logger.close()

    def call(self, *args, **kwargs):
        raise NotImplementedError('Not implemented.')
