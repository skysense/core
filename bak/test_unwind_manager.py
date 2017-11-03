import unittest

from connectivity.bitstamp_api import BitstampAPI
from trader.unwind_management import UnwindManager


class TestUnwind(unittest.TestCase):
    def test_unwind(self):
        b = BitstampAPI()
        u = UnwindManager(bitstamp_api=b)

        u.poll()


if __name__ == '__main__':
    unittest.main()
