import abc

import numpy as np

from model.model_helpers import ModelOutput


class Model:
    def __init__(self):
        pass

    @abc.abstractmethod
    def call(self, *args, **kwargs):
        raise Exception('Abstract method.')


class RandomCoinModel(Model):
    def __init__(self):
        super().__init__()

    def call(self, *args, **kwargs):
        buy = np.random.rand()
        return ModelOutput(buy_confidence=buy, sell_confidence=1 - buy)
