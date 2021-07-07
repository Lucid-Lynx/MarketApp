import logging

from datetime import date
from web.client import Client
from data.store import Store
from utility.config import DEFAULT_BASE_CURRENCY

logging.basicConfig(level=logging.INFO)


class View:

    def __init__(
            self, base_cur=DEFAULT_BASE_CURRENCY, target_cur=DEFAULT_BASE_CURRENCY,
            target_date=date.today().strftime('%d.%m.%Y'), mode='Remote'):
        self.base_cur = base_cur
        self.target_cur = target_cur
        self.target_date = target_date
        self.mode = mode
        self.store = Store(base_currency=self.base_cur, data=None)

        self.__rate = 0

    @property
    def rate(self):
        return self.__rate

    def get_rate(self):
        rate_data = self.store.rates.get(self.target_cur)
        self.__rate = self.store.rates[self.target_cur].rate if rate_data else 0

    def update_data(self):
        self.store = Store(base_currency=self.base_cur, data=self.load_rates())

    def load_rates(self):
        if self.mode == 'Remote':
            resp = Client(date=self.target_date).get_curr_base()
        else:
            resp = Client().get_curr_from_file()

        return resp

    def get_available_bases(self):
        return self.store.available_currencies if len(self.store.available_currencies) else [DEFAULT_BASE_CURRENCY]

    def get_available_targets(self):
        if len(self.store.available_currencies):
            available_targets = self.store.available_currencies.copy()
            available_targets.remove(self.base_cur)

            return available_targets

        else:
            return [DEFAULT_BASE_CURRENCY]

    '''
    def get_rate(self):
        if self.mode == 'File':
            resp = Client(currencies=self.target_cur).get_curr_from_file()
        else:
            resp = Client(currencies=self.target_cur, date=self.target_date).get_curr_base()

        logging.info(resp)
        self.rate = resp['currencies'][self.target_cur]['base_value']
    '''
