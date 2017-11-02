import logging
import threading
from datetime import datetime
from time import sleep

from connectivity.bitstamp_api import BitstampAPI
from connectivity.feeds import NewsAPI
from connectivity.throttling import Throttling
from model.model import RandomCoinModel
from model.model_action_taker import ModelActionTaker
from trader.order_management import OrderManager
from trader.persistence import Persistence
from trader.unwind_management import UnwindManager

print('Program has started.')

PROD_FLAG = False

LOG_FORMAT = '%(asctime)s - %(name)15s - %(levelname)s - %(message)s'

if PROD_FLAG:
    print('Check the log file trading_*.log if nothing is displayed in the console.')
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT,
                        filename='trading_{}.log'.format(datetime.now()))
else:
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT)


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
        self.persistence = Persistence(self.market_api)
        self.unwind_manager = UnwindManager(self.market_api, self.persistence)
        self.oms = OrderManager(self.market_api, self.throttle, self.persistence)
        self.model_action_taker = ModelActionTaker(self.oms)

        self.market_api.start()
        self.unwind_manager.start()
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
        threads = [self.market_api, self.unwind_manager]
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
    trd = Trading()
    trd.run()


if __name__ == '__main__':
    run()
