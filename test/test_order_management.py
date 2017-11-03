import unittest
from time import sleep

from connectivity.bitstamp_api import BitstampAPI
from connectivity.throttling import Throttling
from trader.order_passing_system import OrderPassingSystem


class TestOrderManagement(unittest.TestCase):
    def test_oms(self):
        b = BitstampAPI()
        t = Throttling()
        oms = OrderPassingSystem(bitstamp_api=b, throttle=t)
        oms.send_mass_cancel()
        sleep(15)
        # try to buy one BTC at 5.5 EUR. It's a resting order. We're going to cancel it after that.
        b.buy_limit_order(amount=1, price=5.5)
        assert len(b.open_orders()) == 1
        oms.send_mass_cancel()
        sleep(15)
        assert len(b.open_orders()) == 0

        b.buy_limit_order(amount=1, price=5.6)
        b.buy_limit_order(amount=1, price=5.7)
        assert len(b.open_orders()) == 2
        oms.send_mass_cancel()
        sleep(15)
        assert len(b.open_orders()) == 0


if __name__ == '__main__':
    unittest.main()
