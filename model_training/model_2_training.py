import os
from collections import deque
from time import time

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.contrib.slim as slim
from sklearn.model_selection import TimeSeriesSplit
from tensorflow.contrib.rnn.python.ops.rnn_cell import PhasedLSTMCell

from model.model import Model
from model.model_helpers import stacked_lstm, ModelFileLogger, split_prices, get_batch
from helpers.utils import compute_returns


class Model2(Model):
    def __init__(self):
        super().__init__()
        self.log_file = os.path.join('log', 'log.tsv')
        self.hidden_size = 1024
        self.num_layers = 4
        self.batch_size = 64
        self.steps = 1000
        self.cv_steps = 50

        self.sequence_length = 30  # for now let's do like this.
        self.learning_rate = 5e-7
        print(self.hidden_size)
        print(self.batch_size)
        print(self.steps)
        print(self.learning_rate)
        print(self.sequence_length)

        tf.set_random_seed(1)
        np.random.seed(1)

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
                               num_lstm_layers=self.num_layers,
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

        config = tf.ConfigProto(log_device_placement=False)
        config.gpu_options.per_process_gpu_memory_fraction = 0.97  # because ubuntu desktop uses gpu for xorgs etc
        self.sess = tf.Session(config=config)
        self.sess.run(tf.global_variables_initializer())

    def train(self, replay_file=os.path.join('data_examples', 'btc_price_2017-09-13T03:45:28+00:00.csv')):
        # DATA PART #######################
        # removing the columns where the last price did not move. It biases the model.
        prices = pd.read_csv(replay_file, index_col=0, parse_dates=True)
        prices['last'] = prices[['last']].astype(np.float)
        prices['last'] = compute_returns(prices['last'])
        prices = prices[prices['last'] != 0]
        # splitting training, cv, test set
        prices_train, prices_cv, prices_test = split_prices(prices)

        # RUN PART #######################
        running_difference_tr = deque(maxlen=100)
        running_accuracy_tr = deque(maxlen=100)
        running_difference = deque(maxlen=100)
        running_accuracy = deque(maxlen=100)
        running_difference_cv = deque(maxlen=100)
        running_accuracy_cv = deque(maxlen=100)

        tscv = TimeSeriesSplit(n_splits=self.steps)

        for i, (train_index, cv_index) in enumerate(tscv.split(prices_train)):
            prices_train_fold = prices_train.iloc[train_index, :]
            prices_cv_fold = prices_train.iloc[cv_index, :]

            # gradient update
            x_train, t_train, y_train = get_batch(self.batch_size, prices_train_fold, self.sequence_length)
            st = time()
            _, te_loss_tr, be_loss_tr = self.sess.run([self.train_step, self.loss, self.benchmark_loss],
                                                      feed_dict={self.x_: x_train,
                                                                 self.y_: y_train,
                                                                 self.t_: t_train})  # gradient update.

            running_difference_tr.append(be_loss_tr - te_loss_tr)
            running_accuracy_tr.append(te_loss_tr < be_loss_tr)
            print(
                'steps = {0} | time {1:.3f} | te_loss_tr = {2:.6f}, be_loss_tr = {3:.6f}, r_diff_tr = {4:.6f}, r_acc_tr = {5:.3f}'.format(
                    str(i).zfill(6), time() - st, te_loss_tr, be_loss_tr, np.mean(running_difference_tr),
                    np.mean(running_accuracy_tr)))
            self.file_logger.write(
                [i, te_loss_tr, be_loss_tr, np.mean(running_difference_tr), np.mean(running_accuracy_tr)])

            # cross validation after gradient update step
            x_test, t_test, y_test = get_batch(self.batch_size, prices_cv_fold, self.sequence_length)
            te_loss, be_loss = self.sess.run([self.loss, self.benchmark_loss],
                                             feed_dict={self.x_: x_test,
                                                        self.y_: y_test,
                                                        self.t_: t_test})
            running_difference.append(be_loss - te_loss)
            running_accuracy.append(te_loss < be_loss)
            print(
                'steps = {0} | time {1:.3f} | te_loss_cv = {2:.6f}, be_loss_cv = {3:.6f}, r_diff_cv = {4:.6f}, r_acc_cv = {5:.3f}'.format(
                    str(i).zfill(6), time() - st, te_loss, be_loss, np.mean(running_difference),
                    np.mean(running_accuracy)))
            self.file_logger.write([i, te_loss, be_loss, np.mean(running_difference), np.mean(running_accuracy)])

        # cross validation after done training
        for i in range(self.cv_steps):
            x_cv, t_cv, y_cv = get_batch(self.batch_size, prices_cv, self.sequence_length)
            cv_loss, be_loss = self.sess.run([self.loss, self.benchmark_loss],
                                             feed_dict={self.x_: x_cv,
                                                        self.y_: y_cv,
                                                        self.t_: t_cv})

            running_difference_cv.append(be_loss - cv_loss)
            running_accuracy_cv.append(cv_loss < be_loss)
        print(
            'CV | cv_loss = {0:.6f}, be_loss = {1:.6f}, r_diff = {2:.6f}, r_acc = {3:.3f}'.format(
                cv_loss, be_loss, np.mean(running_difference_cv), np.mean(running_accuracy_cv)))
        self.file_logger.write([i, cv_loss, be_loss, np.mean(running_difference_cv), np.mean(running_accuracy_cv)])

        self.file_logger.close()

    def call(self, *args, **kwargs):
        raise NotImplementedError('Not implemented.')
