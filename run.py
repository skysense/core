import threading

from connectivity.bitstamp_api import BitstampAPI
from connectivity.feeds import NewsAPI


class Trading:
    def __init__(self):
        self.market_api = BitstampAPI()
        self.news_api = NewsAPI()
        self.market_api.register_observer(self)
        self.news_api.register_observer(self)

        self.market_api.start()
        self.news_api.start()
        self.lock = threading.Lock()

    def news_notification(self, observable, *args, **kwargs):
        print('Received NEWS message from : ', observable)

    def price_update_notification(self, observable, *args, **kwargs):
        print('Received PRICE UPDATE message from : ', observable)

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
