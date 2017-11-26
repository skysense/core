import tensorflow as tf
import tensorflow.contrib.slim as slim
from easy_model_saving import model_saver

from constants import MODEL_INPUT_TENSOR_NAME, MODEL_OUTPUT_TENSOR_NAME, MODEL_CHECKPOINTS_DIR


def graph():
    input_close_prices = tf.placeholder(tf.float32, shape=[None, 1], name=MODEL_INPUT_TENSOR_NAME)
    m = slim.fully_connected(inputs=input_close_prices, num_outputs=20, activation_fn=tf.nn.relu)
    softmax_output = slim.fully_connected(inputs=m, num_outputs=3, activation_fn=tf.nn.softmax)
    tf.identity(softmax_output, name=MODEL_OUTPUT_TENSOR_NAME)


def run_dummy_training():
    with tf.Session() as sess:
        graph()
        sess.run(tf.global_variables_initializer())
        saver = model_saver.Saver(MODEL_CHECKPOINTS_DIR)
        saver.save(global_step=10)

        last_step = model_saver.restore_graph_variables(MODEL_CHECKPOINTS_DIR)
        assert last_step != 0


if __name__ == '__main__':
    run_dummy_training()
