import logging
import os
import threading
from datetime import datetime
from time import sleep

from connectivity.bitstamp_api import BitstampAPI
from connectivity.order_passing_system import OrderPassingSystem
from connectivity.throttling import Throttling
from constants import ADMIN_LOG_FORMAT, ADMIN_PROD_FLAG, MODEL_WARM_UP_PHASE_NUM_TICKS
from model.model import RandomCoinModel
from model.model_action_taker import ModelActionTaker
from model.model_data_recorder import ModelDataRecorder


class Trading:
    def __init__(self):
        self.logger = logging.getLogger('MainThread')
        self.lock = threading.Lock()
        self.model_prices = RandomCoinModel()
        self.model_news = RandomCoinModel()
        self.market_api = BitstampAPI()
        self.market_api.register_observer(self)
        self.throttle = Throttling()
        self.order_passing = OrderPassingSystem(self.market_api, self.throttle)
        self.model_action_taker = ModelActionTaker(self.order_passing)
        self.model_data_recorder = ModelDataRecorder()

        self.workers = [self.market_api]

        for worker in self.workers:
            worker.start()

    def price_update_notification(self, ticker_update):
        self.model_data_recorder.update(ticker_update)
        data = self.model_data_recorder.get_data_frame()

        if len(data) < MODEL_WARM_UP_PHASE_NUM_TICKS:
            self.logger.warn('Warming up. Waiting to reach {0} '
                             'ticker updates before calling models.'.format(MODEL_WARM_UP_PHASE_NUM_TICKS))
        else:
            model_output = self.model_prices.call(data)
            self.logger.info('Prices model output on new data : {0}'.format(model_output))
            trading_action = self.model_action_taker.take_trading_action(model_output)
            if trading_action is None:
                self.logger.info('No trading action was taken on this price update.')
            else:
                self.logger.info('Initiated an order: {0}'.format(trading_action))

    def notify(self, observable, *args, **kwargs):
        self.lock.acquire()
        observable_type = type(observable)
        try:
            if observable_type is BitstampAPI:
                self.logger.info('Received PRICE UPDATE message from : {0} with args: {1}'.format(observable, args))
                ticker_update = args[0]['ticker']
                self.price_update_notification(ticker_update)
            else:
                raise Exception('Unknown type.')
        except Exception as e:
            raise e
        finally:
            self.lock.release()

    def run(self):
        keyboard_trigger_stop = False
        while True:
            try:
                if keyboard_trigger_stop:
                    for t in self.workers:
                        t.terminate()
                        t.join()
                    break
                for t in self.workers:
                    if not t.is_alive():
                        self.logger.error('{0} is dead. Program will exit.'.format(t))
                        for t2 in self.workers:
                            t2.terminate()
                            t2.join()
                        break
                sleep(0.1)
            except KeyboardInterrupt:
                keyboard_trigger_stop = True


def run():
    print('Program has started.')

    if ADMIN_PROD_FLAG:
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
