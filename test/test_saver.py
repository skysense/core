import os
import shutil
import tempfile
import unittest
from glob import glob

import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim

from model import model_saver


def ensure_path_tf(folder):
    if not tf.gfile.Exists(folder):
        tf.gfile.MakeDirs(folder)
    return folder


def ensure_join_path(*path_list):
    return ensure_path_tf(os.path.join(*path_list))


def cnn_block(net, features, param, scope):
    with tf.variable_scope(scope):
        net = slim.repeat(net, param.cnn_convolutions, slim.conv2d, features, param.cnn_convolution_kernel,
                          padding=param.cnn_convolution_padding,
                          activation_fn=param.cnn_convolution_activation,
                          scope='Convolution')
        net = slim.max_pool2d(net, param.cnn_max_pool_kernel, padding=param.cnn_max_pool_padding, scope='MaxPool')
    return net


class Parameters:
    image_x_len = 28
    image_y_len = 28
    output_features = 10

    cnn_blocks = 2
    cnn_features_initial = 64
    cnn_features_block_multiply = 2

    cnn_convolutions = 2
    cnn_convolution_kernel = (3, 3)
    cnn_convolution_padding = 'SAME'
    cnn_convolution_activation = tf.nn.relu
    cnn_max_pool_kernel = (2, 2)
    cnn_max_pool_padding = 'SAME'


def graph(batch_size=None, param=Parameters):
    with tf.variable_scope('Input'):
        x_ = tf.placeholder(tf.float32, [batch_size, param.image_x_len * param.image_y_len], name='Image')
        y_ = tf.placeholder(tf.float32, [batch_size, param.output_features], name='Label')

    with tf.variable_scope('ToCNN'):
        x_image = tf.reshape(x_, [-1, param.image_x_len, param.image_y_len, 1], name='2DImage')

    with tf.variable_scope('CNN'):
        cnn_features = param.cnn_features_initial
        cnn = x_image
        for i in range(param.cnn_blocks):
            cnn = cnn_block(cnn, cnn_features, param, 'Block_' + repr(i + 1))
            cnn_features *= param.cnn_features_block_multiply

    with tf.variable_scope('ToOutput'):
        cnn_flattened = slim.flatten(cnn, scope='FlatCNNOutput')
        unscaled_logit = slim.fully_connected(cnn_flattened, param.output_features,
                                              activation_fn=None,
                                              scope='UnscaledLogit')

    with tf.variable_scope('Output'):
        label_probability = tf.nn.softmax(unscaled_logit, name='Probability')
        label_prediction = tf.argmax(label_probability, 1, name='Prediction')

    with tf.variable_scope('Loss'):
        tf.identity(tf.losses.softmax_cross_entropy(y_, unscaled_logit), name='CrossEntropy')

    with tf.variable_scope('Metric'):
        correct_predictions = tf.equal(label_prediction, tf.argmax(y_, 1), name='Correct')
        tf.reduce_mean(tf.cast(correct_predictions, tf.float32), name='Accuracy')


class TestSaver(unittest.TestCase):
    def test_model_saving(self):
        root_path = tempfile.gettempdir()
        checkpoint_path = ensure_join_path(root_path, 'checkpoint')
        try:
            shutil.rmtree(checkpoint_path)
        except FileNotFoundError:
            pass
        with tf.Session() as sess:
            graph()

            last_step = model_saver.restore_graph_variables(checkpoint_path)
            assert last_step == 0
            if last_step == 0:
                model_saver.initialize_graph_variables()

            stat_1 = np.sum(sess.run(tf.trainable_variables())[0].flatten())
            saver = model_saver.Saver(checkpoint_path)

            i = 1
            for global_step in range(last_step, last_step + 10):
                saver.save(global_step=global_step)
                assert len(glob(checkpoint_path + '/*.meta', recursive=True)) == i
                i += 1

        tf.reset_default_graph()
        with tf.Session() as sess:
            graph()
            last_step = model_saver.restore_graph_variables(checkpoint_path)
            assert last_step == 9
            if last_step == 0:
                model_saver.initialize_graph_variables()

            stat_2 = np.sum(sess.run(tf.trainable_variables())[0].flatten())

            assert stat_1 == stat_2

            saver = model_saver.Saver(checkpoint_path)

            i = last_step + 1
            for global_step in range(last_step, last_step + 10):
                saver.save(global_step=global_step)
                assert len(glob(checkpoint_path + '/*.meta', recursive=True)) == i
                i += 1

        try:
            shutil.rmtree(checkpoint_path)
        except FileNotFoundError:
            pass
        tf.reset_default_graph()
        with tf.Session() as sess:
            graph()
            last_step = model_saver.restore_graph_variables(checkpoint_path)
            assert last_step == 0
            if last_step == 0:
                model_saver.initialize_graph_variables()

            stat_3 = np.sum(sess.run(tf.trainable_variables())[0].flatten())

            assert stat_1 != stat_3


if __name__ == '__main__':
    unittest.main()
