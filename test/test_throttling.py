import unittest
from time import sleep

from connectivity.throttling import Throttling


class TestThrottling(unittest.TestCase):
    def test_throttling(self):
        t = Throttling(raise_exception=False)
        assert t.check_validity()  # first request should go through.
        assert not t.check_validity()  # then should block.
        sleep(t.minimum_interval_between_two_requests + 1)
        assert t.check_validity()  # then should go through.
        assert not t.check_validity()  # then should block again.
        sleep(t.minimum_interval_between_two_requests - 1)
        assert not t.check_validity()  # should block.
        sleep(2)
        assert t.check_validity()  # should go through.


if __name__ == '__main__':
    unittest.main()
