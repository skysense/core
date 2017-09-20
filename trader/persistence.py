import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Persistence:
    def __init__(self):
        self.filename = '../persisted_orders.json'

    def read_from_persistence(self):
        if not os.path.isfile(self.filename):
            return {}
        else:
            with open(self.filename, 'r') as fp:
                return json.load(fp)

    def persist(self, order_id, amount, price, way):
        persisted_orders = self.read_from_persistence()
        order = {'amount': amount,
                 'price': price,
                 'way': way}
        logging.info('About to persist order = {0} with ID = {1}'.format(order, order_id))
        if order_id in persisted_orders:
            raise Exception('Order ID conflict for {}.'.format(order_id))
        if not (way == 'buy' or way == 'sell'):
            raise Exception('Way should be either buy or sell.')
        persisted_orders[order_id] = order
        with open(self.filename, 'w') as fp:
            json.dump(persisted_orders, fp, ensure_ascii=True, indent=4)


if __name__ == '__main__':
    persistence = Persistence()
    persistence.persist('OS124', 1, 10, 'buy')
    persistence.persist('OS125', 3, 20, 'buy')
    persistence.persist('OS126', 2, 30, 'sell')
