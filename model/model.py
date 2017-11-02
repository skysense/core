import abc


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
        # TODO: hard coded for reproducibility.
        return {'buy_confidence': 0.4, 'sell_confidence': 0.6}
