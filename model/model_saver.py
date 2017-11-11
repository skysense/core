import os
import re
from glob import glob

import tensorflow as tf


def get_tensor_by_name(tensor_or_operation, index=0):
    graph = tf.get_default_graph()
    if index is not None:
        tensor_or_operation += ':' + repr(index)
        return graph.get_tensor_by_name(tensor_or_operation)
    else:
        return graph.get_operation_by_name(tensor_or_operation)


class Saver:
    def __init__(self, save_path, max_to_keep=100):
        self._save_path = save_path
        self._saver = tf.train.Saver(max_to_keep=max_to_keep)

    def save(self, sess=None, global_step=None):
        if sess is None:
            sess = tf.get_default_session()
        save_path_name = os.path.join(self._save_path, 'step')
        self._saver.save(sess, save_path_name, global_step=global_step)


def last_checkpoint(load_path):
    checkpoints = glob(os.path.join(load_path, 'step-*'))
    p = re.compile('(.*step-[0-9]*)')
    checkpoints = [p.search(f).group(1) for f in checkpoints]
    checkpoints = sorted(checkpoints, key=lambda x: int(x.split('-')[-1]))
    return checkpoints[-1] if checkpoints else None


def restore_graph_variables(load_path, filename=None):
    if not filename:
        checkpoint = last_checkpoint(load_path)
    else:
        checkpoint = os.path.join(load_path, filename)
    sess = tf.get_default_session()
    if checkpoint is None:
        return 0
    loader = tf.train.Saver(var_list=None)
    loader.restore(sess, checkpoint)
    return int(re.search('step-[0-9]+', checkpoint).group(0).split('-')[-1])


def initialize_graph_variables():
    sess = tf.get_default_session()
    sess.run(tf.global_variables_initializer())
