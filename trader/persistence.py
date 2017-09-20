import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Persistence:
    def __init__(self, bitstamp_api=None):
        self.filename = '../persisted_orders.json'
        self.bitstamp_api = bitstamp_api

    def read_from_persistence(self):
        if not os.path.isfile(self.filename):
            return {}
        else:
            with open(self.filename, 'r') as fp:
                return json.load(fp)

    def enrich_persisted_orders_with_market_statuses(self, persisted_orders):
        if self.bitstamp_api is None:
            return persisted_orders
        for order_id in sorted(persisted_orders.keys()):
            status = self.bitstamp_api.order_status(order_id)
            persisted_orders[order_id]['status'] = status
        return persisted_orders

    def persist(self, order_id, amount, price, way):
        persisted_orders = self.enrich_persisted_orders_with_market_statuses(self.read_from_persistence())
        order = {'amount': amount,
                 'price': price,
                 'way': way}
        logging.info('About to persist order = {0} with ID = {1}'.format(order, order_id))
        if order_id in persisted_orders:
            raise Exception('Order ID conflict for {0}.'.format(order_id))
        if not (way == 'buy' or way == 'sell'):
            raise Exception('Way should be either buy or sell.')
        persisted_orders[order_id] = order
        with open(self.filename, 'w') as fp:
            json.dump(persisted_orders, fp, ensure_ascii=True, indent=4)

    def request_order_from_persistence(self, order_id):
        persisted_orders = self.enrich_persisted_orders_with_market_statuses(self.read_from_persistence())
        if order_id not in persisted_orders:
            raise Exception('Could not find Order ID {0} in the persistence.'.format(order_id))
        return persisted_orders[order_id]


if __name__ == '__main__':
    persistence = Persistence()
    logging.info(persistence.request_order_from_persistence('OS125'))
    persistence.persist('OS124', 1, 10, 'buy')
    persistence.persist('OS125', 3, 20, 'buy')
    persistence.persist('OS126', 2, 30, 'sell')
