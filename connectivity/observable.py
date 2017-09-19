import abc
import threading
from time import sleep


class Observable:
    def __init__(self):
        self.__observers = []
        self.thread = threading.Thread(target=self.run)
        self.polling_interval = 2  # in seconds

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)

    def start(self):
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            results = self.poll()
            if results is not None:
                self.notify_observers(results)
            sleep(self.polling_interval)

    @abc.abstractmethod
    def poll(self):
        raise Exception('Abstract Method.')

    def join(self):
        self.thread.join()
