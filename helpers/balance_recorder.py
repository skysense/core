import os
from datetime import datetime


class BalanceRecorder:
    def __init__(self):
        self.balance_tracking_file = os.path.join('log', 'balance_{0}.log'.format(datetime.now()))
        self.headers = []

    def update(self, market_api_balance):
        d = {k: str(float(round(v, 8))) for (k, v) in market_api_balance.items()}
        d = {k: v for k, v in d.items() if 'available' in k or 'balance' in k}

        if len(self.headers) == 0:
            self.headers = list(sorted(d.keys()))
            self.write(self.headers)

        csv_values = [d[k] for k in self.headers]
        self.write(csv_values)

    def write(self, csv_values):
        formatting = ''.join(['{:<15} | ' for _ in range(len(self.headers))])
        csv_row = formatting.format(*csv_values)
        with open(self.balance_tracking_file, 'a+') as w:
            w.write(csv_row)
            w.write('\n')
