import abc

import numpy as np


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
        return np.random.rand()
