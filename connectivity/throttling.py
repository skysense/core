from time import time


class Throttling:
    def __init__(self, raise_exception=True):
        self.minimum_interval_between_two_requests = 10  # seconds
        self.timestamp_last_valid_throttling_call = time() - self.minimum_interval_between_two_requests
        self.raise_exception = raise_exception

    def check_validity(self):
        now = time()
        if now - self.timestamp_last_valid_throttling_call > self.minimum_interval_between_two_requests:
            self.timestamp_last_valid_throttling_call = now
            return True
        else:
            if self.raise_exception:
                err = 'Throttling. You are sending too many requests. Max one every {0} seconds.'.format(
                    self.minimum_interval_between_two_requests)
                raise Exception(err)
            return False
