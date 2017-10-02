# will contain=
# - re player for bid-ask prices.
# - basic in memory logic database and so on


class UserAccount:
    def __init__(self):
        self.btc_available = 0.00000000
        self.btc_balance = 0.00000000

        self.btc_reserved = 0.00000000
        self.btceur_fee = 0.25
        self.btcusd_fee = 0.25

        self.eth_available = 0.00000000
        self.eth_balance = 0.00000000
        self.eth_reserved = 0.00000000
        self.ethbtc_fee = 0.00
        self.etheur_fee = 0.00

        self.ethusd_fee = 0.00
        self.eur_available = 105

        self.eur_balance = 105
        self.eur_reserved = 0.00

        self.eurusd_fee = 0.25
        self.ltc_available = 0.00000000
        self.ltc_balance = 0.00000000

        self.ltc_reserved = 0.00000000
        self.ltcbtc_fee = 0.25

        self.ltceur_fee = 0.25
        self.ltcusd_fee = 0.25

        self.usd_available = 0.00
        self.usd_balance = 0.00

        self.usd_reserved = 0.00
        self.xrp_available = 0.00000000

        self.xrp_balance = 0.00000000
        self.xrp_reserved = 0.00000000

        self.xrpbtc_fee = 0.25
        self.xrpeur_fee = 0.25
        self.xrpusd_fee = 0.25

        # first transaction is the payment.
        self.transactions = [
            {'fee': '0.00', 'btc_usd': '0.00', 'datetime': '2017-09-22 08:45:10', 'usd': 0.0, 'btc': 0.0, 'type': '0',
             'id': 22034181, 'eur': '105.00'}]

        # {'price': Decimal('2470.22'), 'currency_pair': 'BTC/EUR',
        # 'datetime': datetime.datetime(2017, 9, 24, 10, 50, 50), 'amount': Decimal('0.00300000'),
        # 'type': '0', 'id': '320422620'}
        self.open_orders = []

        self.order_statuses = []
