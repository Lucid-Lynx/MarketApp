import logging

from datetime import date
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from parser_tools.parser import Parser
from .currency import Currency

logging.basicConfig(level=logging.INFO)


class Record:

    def __init__(self, base_currency=DEFAULT_BASE_CURRENCY, data=None, current_date=date.today().strftime(DATE_FORMAT)):
        self.base_currency = base_currency

        parsed_data = Parser(text=data).get_curr_info() if data else None

        self.current_date = current_date
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

    def change_base_currency(self, base_currency=DEFAULT_BASE_CURRENCY):
        self.base_currency = base_currency
        base_currency_rate = self.rates[base_currency].rate

        for currency in self.rates.values():
            currency.change_base_currency(base_currency=base_currency, base_rate=base_currency_rate)
