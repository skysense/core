import abc
import logging
import threading
from time import sleep


class SingletonObservable:
    def __init__(self, clazz):
        if clazz._instance is not None:
            raise Exception('Singleton error. More than one instance was registered for {0}'.format(self))
        clazz._instance = self
        self.clazz = clazz
        self.__observers = []
        clazz_name = str(clazz._instance).split('.')[-1].split(' ')[0]  # inspection
        self.logger = logging.getLogger(clazz_name)
        self.thread = threading.Thread(target=self.run, name=clazz_name)
        self.polling_interval = 5  # in seconds
        self.stop = False

    def is_alive(self):
        return self.thread.is_alive()

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)

    def start(self):
        self.thread.daemon = True
        self.thread.start()
        self.logger.info('Thread [{0}] started.'.format(self.clazz))

    def run(self):
        while not self.stop:
            results = self.poll()
            if results is not None:
                self.notify_observers(results)
            sleep(self.polling_interval)

    @abc.abstractmethod
    def poll(self):
        raise Exception('Abstract Method.')

    def terminate(self):
        self.stop = True

    def join(self):
        self.thread.join()
