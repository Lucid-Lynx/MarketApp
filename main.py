#!/usr/bin/python3
import sys
import logging

from datetime import date
from decimal import setcontext, Context, ROUND_HALF_EVEN, Decimal
from web.client import Client
from utility.config import PREC, DEFAULT_BASE_CURRENCY, DATE_FORMAT
from data.record import Record
from data.loader import run_in_background

logging.basicConfig(level=logging.INFO)


class Workflow:
    """
    Main class with workflow methods
    """

    def __init__(self, target_cur: str = DEFAULT_BASE_CURRENCY,  mode: str = 'Remote'):
        self.__base_cur = DEFAULT_BASE_CURRENCY
        self.target_cur = target_cur
        self.mode = mode

    @property
    def base_cur(self) -> str:
        return self.__base_cur

    def get_data(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> Record:
        """
        Get record from cache by date
        :param target_date: target date for data to store: str
        :return: new record: Record
        """

        return Record(data=self.load_rates(target_date=target_date), current_date=target_date) \
            if self.mode == 'Remote' else \
            Record(data=Client(date=target_date).get_curr_from_file(), current_date=target_date)

    @staticmethod
    @run_in_background
    def load_rates(target_date: str = date.today().strftime(DATE_FORMAT)) -> str:
        """
        Load new data with rates from remote source or file
        :param target_date: target date: str
        :return: text response: str
        """

        return Client(date=target_date).get_curr_base()

    def get_rate(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> (int, Decimal):
        """
        Get rate data from cache
        :param target_date: target date: str
        :return: currency rate: int, Decimal
        """

        record = self.get_data(target_date=target_date)

        if not record:
            return 0

        base_rate_data = record.rates.get(self.base_cur)
        target_rate_data = record.rates.get(self.target_cur)
        return target_rate_data.rate / base_rate_data.rate if base_rate_data and target_rate_data else 0


def app():
    """
    Main application loop. Runs menu
    :return: None
    """

    print('Choose currency or skip:')
    currency = input().strip()

    if not currency:
        err = 'Currency is not chosen. Please, input target currency'
        raise ValueError(err)

    print('Choose mode: file or remote:')
    mode = input().strip()

    if mode not in ['file', 'remote']:
        err = 'Invalid mode'
        raise ValueError(err)

    if mode == 'file':
        resp = Workflow(target_cur=currency, mode='File').get_rate()
    else:
        print('Input date in format DD.MM.YYYY or skip:')
        target_date = input().strip() or date.today().strftime(DATE_FORMAT)
        resp = Workflow(target_cur=currency).get_rate(target_date=target_date)

    print(f'Rate {currency}/{DEFAULT_BASE_CURRENCY}: {resp}')


def main():
    """
    Application entry point
    :return: None
    """

    context = Context(prec=PREC, rounding=ROUND_HALF_EVEN)
    setcontext(context)

    while True:
        print('Exit? Write "y" or skip')
        is_exit = input().strip() == 'y'

        if is_exit:
            print('App work is finished')
            break

        try:
            app()

        except ValueError as err:
            print(err)
            continue

        except Exception as err:
            logging.error(err, exc_info=True)
            sys.exit(1)


if __name__ == '__main__':
    main()
