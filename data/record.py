from datetime import date
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from parser_tools.parser import Parser
from .currency import Currency


class Record:
    """
    Class for cache record
    """

    def __init__(
            self, base_currency: str = DEFAULT_BASE_CURRENCY, data: str = None,
            current_date: str = date.today().strftime(DATE_FORMAT)):
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

    def change_base_currency(self, base_currency: str = DEFAULT_BASE_CURRENCY):
        """
        Set new base currency
        :param base_currency: new base currency: str
        :return:
        """

        self.base_currency = base_currency
        base_currency_rate = self.rates[base_currency].rate

        for currency in self.rates.values():
            currency.change_base_currency(base_currency=base_currency, base_rate=base_currency_rate)
