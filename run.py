import logging
import threading
from datetime import datetime
from time import sleep
import os
from connectivity.bitstamp_api import BitstampAPI
from connectivity.feeds import NewsAPI
from connectivity.order_passing_system import OrderPassingSystem
from connectivity.throttling import Throttling
from constants import ADMIN_LOG_FORMAT, ADMIN_LOG_PROD_FLAG
from model.model import RandomCoinModel
from model.model_action_taker import ModelActionTaker


class Trading:
    def __init__(self):
        self.logger = logging.getLogger('MainThread')
        self.lock = threading.Lock()
        self.model_prices = RandomCoinModel()
        self.model_news = RandomCoinModel()
        self.market_api = BitstampAPI()
        self.news_api = NewsAPI()
        self.market_api.register_observer(self)
        self.news_api.register_observer(self)
        self.throttle = Throttling()
        self.oms = OrderPassingSystem(self.market_api, self.throttle)
        self.model_action_taker = ModelActionTaker(self.oms)

        self.market_api.start()
        # self.news_api.start() - register it later. TODO: implement it and use NLP here.

    def news_notification(self, observable, *args, **kwargs):
        self.logger.info('Received NEWS message from : {0}'.format(observable))
        model_output = self.model_news.call(args, kwargs)
        self.logger.info('New model output on new data : {0}'.format(model_output))
        self.model_action_taker.take_trading_action(model_output)

    def price_update_notification(self, observable, *args, **kwargs):
        self.logger.info('Received PRICE UPDATE message from : {0} with args: {1}'.format(observable, args))
        model_output = self.model_prices.call(args, kwargs)
        self.logger.info('Prices model output on new data : {0}'.format(model_output))
        self.model_action_taker.take_trading_action(model_output)

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
        threads = [self.market_api]
        stop_main = False
        while not stop_main:
            for t in threads:
                if not t.is_alive():
                    self.logger.error('{0} is dead. Program will exit.'.format(t))
                    for t2 in threads:
                        t2.terminate()
                        t2.join()
                    stop_main = True
            sleep(0.1)


def run():
    print('Program has started.')

    if ADMIN_LOG_PROD_FLAG:
        log_filename = os.path.join('log', 'trading_{0}.log'.format(datetime.now()))
        print('Check the log file {0} if nothing is displayed in the console.'.format(log_filename))
        logging.basicConfig(level=logging.INFO,
                            format=ADMIN_LOG_FORMAT,
                            filename=log_filename)
    else:
        logging.basicConfig(level=logging.INFO,
                            format=ADMIN_LOG_FORMAT)
    trd = Trading()
    trd.run()


if __name__ == '__main__':
    run()
