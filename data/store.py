import logging

from datetime import date
from utility.config import DEFAULT_BASE_CURRENCY
from parser.parser import Parser
from .currency import Currency

logging.basicConfig(level=logging.INFO)


class Store:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Store, cls).__new__(cls)

        return cls.instance

    def __init__(self, base_currency=DEFAULT_BASE_CURRENCY, data=None):
        self.base_currency = base_currency

        parsed_data = Parser(text=data).get_curr_info() if data else None

        self.current_date = parsed_data['date'] if parsed_data else date.today().strftime('%d.%m.%Y')
        self.available_currencies = [DEFAULT_BASE_CURRENCY]
        self.rates = {
            DEFAULT_BASE_CURRENCY: Currency(),
        }

        if parsed_data:
            self.available_currencies += [key for key in parsed_data['currencies'].keys()]
            self.rates.update({
                key: Currency(
                    code=parsed_data['currencies'][key]['alpha_code'],
                    quantity=parsed_data['currencies'][key]['quantity'],
                    rate=parsed_data['currencies'][key]['value']) for key in parsed_data['currencies'].keys()
            })

        if self.base_currency != DEFAULT_BASE_CURRENCY:
            self.change_base_currency(base_currency=self.base_currency)

    def change_base_currency(self, base_currency=DEFAULT_BASE_CURRENCY):
        self.base_currency = base_currency
        base_currency_rate = self.rates[base_currency].rate

        for currency in self.rates.values():
            currency.change_base_currency(base_currency=base_currency, base_rate=base_currency_rate)
