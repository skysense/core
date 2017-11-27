import abc
from glob import glob

import numpy as np
import tensorflow as tf
from easy_model_saving import model_saver

from constants import MODEL_CHECKPOINTS_DIR, MODEL_INPUT_TENSOR_NAME, MODEL_OUTPUT_TENSOR_NAME


class Model:
    def __init__(self):
        pass

    @abc.abstractmethod
    def call(self, *args, **kwargs):
        raise Exception('Abstract method.')


class WeightsNotFoundException(Exception):
    pass


class TensorflowModel(Model):
    def __init__(self):
        super().__init__()
        self.sess = tf.Session()
        # TODO: add it in model_saver later.
        meta_files = sorted(glob(MODEL_CHECKPOINTS_DIR + '/**/*.meta', recursive=True))
        try:
            tf.train.import_meta_graph(meta_files[-1])
        except IndexError:
            raise WeightsNotFoundException(MODEL_CHECKPOINTS_DIR)
        last_step = model_saver.restore_graph_variables(MODEL_CHECKPOINTS_DIR, sess=self.sess)
        if last_step == 0:
            raise WeightsNotFoundException(MODEL_CHECKPOINTS_DIR)

        self.input_tensor = model_saver.get_tensor_by_name(MODEL_INPUT_TENSOR_NAME)
        self.output_tensor = model_saver.get_tensor_by_name(MODEL_OUTPUT_TENSOR_NAME)

    def call(self, *args, **kwargs):
        close_prices = args[0]['last'].values.astype(np.float)
        # TODO: for now it's a bit dumb. We only take the last price into account!
        # It's just to show how to use it for later.
        feed_dict = {self.input_tensor: np.expand_dims([close_prices[-1]], axis=0)}
        out = self.sess.run(self.output_tensor, feed_dict=feed_dict)
        buy, sell, hold = out.flatten()
        return ModelOutput(buy_confidence=buy, sell_confidence=sell, hold_confidence=hold)


class RandomCoinModel(Model):
    def __init__(self):
        super().__init__()

    def call(self, *args, **kwargs):
        # Toy model! It's not even powered by Tensorflow.
        buy, sell, hold = np.random.dirichlet(np.ones(3))
        return ModelOutput(buy_confidence=buy, sell_confidence=sell, hold_confidence=hold)


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
