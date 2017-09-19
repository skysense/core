import threading

from connectivity.bitstamp_api import BitstampAPI
from connectivity.feeds import NewsAPI
from model.model import RandomCoinModel
from trader.order_management import OrderManagement
from connectivity.throttling import Throttling


class Trading:
    def __init__(self):
        self.lock = threading.Lock()
        self.model = RandomCoinModel()
        self.market_api = BitstampAPI()
        self.news_api = NewsAPI()
        self.market_api.register_observer(self)
        self.news_api.register_observer(self)
        self.throttle = Throttling()
        self.oms = OrderManagement(self.market_api, self.throttle)

        self.market_api.start()
        self.news_api.start()

    def news_notification(self, observable, *args, **kwargs):
        print('Received NEWS message from : ', observable)
        buy_confidence = self.model.call(args, kwargs)
        if buy_confidence > 0.5:
            self.oms.send_buy_order(amount=0.01)

    def price_update_notification(self, observable, *args, **kwargs):
        print('Received PRICE UPDATE message from : ', observable)
        self.model.call(args, kwargs)
        buy_confidence = self.model.call(args, kwargs)
        if buy_confidence > 0.5:
            self.oms.send_buy_order(amount=0.01)

    def notify(self, observable, *args, **kwargs):
        self.lock.acquire()
        try:
            notification_type = args[0]['key']
            if notification_type == 'news':
                self.news_notification(observable, args, kwargs)
            elif notification_type == 'price_update':
                self.price_update_notification(observable, args, kwargs)
            else:
                raise Exception('Unknown type : {}'.format(notification_type))
        except Exception as e:
            raise e
        finally:
            self.lock.release()

    def run(self):
        self.market_api.join()
        self.news_api.join()


def run():
    trd = Trading()
    trd.run()


if __name__ == '__main__':
    run()
