#!/usr/bin/python3
import os
import logging

from datetime import datetime
from decimal import setcontext, Context, ROUND_HALF_EVEN
from parser.parser import Parser
from utility.config import PREC, DATE_FORMAT

logging.basicConfig(level=logging.INFO)


class Data:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Data, cls).__new__(cls)

        return cls.instance

    def __init__(self, currencies=None, date=None):
        self.base_path = os.path.relpath(os.path.expanduser('~/Development/Currencies/curr_base.html'))
        self.currencies = currencies

        if date and not Parser.check_date(date=date):
            raise ValueError(f'Invalid date format in "{date}"')

        if date and datetime.strptime(date, DATE_FORMAT) > datetime.now():
            raise ValueError('Incorrect date. Choose today or earlier')

        self.date = date

    def get_curr_from_file(self):
        if not os.path.exists(self.base_path):
            raise FileNotFoundError(f'Currency HTML file "{self.base_path}" does not exist')

        with open(self.base_path, 'r') as f:
            text = f.read()

            return Parser(text=text, currencies=self.currencies).get_curr_info()


def app():
    context = Context(prec=PREC, rounding=ROUND_HALF_EVEN)
    setcontext(context)

    print('Choose currencies or skip:')
    currencies = input()
    currencies = currencies.strip()

    resp = Data(currencies=currencies).get_curr_from_file()
    print(resp)


def main():
    try:
        app()

    except Exception as err:
        logging.error(err)


if __name__ == '__main__':
    main()
