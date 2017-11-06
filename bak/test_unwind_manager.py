import unittest

from trader.unwind_management import UnwindManager

from connectivity.bitstamp_api import BitstampAPI


class TestUnwind(unittest.TestCase):
    def test_unwind(self):
        b = BitstampAPI()
        u = UnwindManager(bitstamp_api=b)
        u.poll()


if __name__ == '__main__':
    unittest.main()
