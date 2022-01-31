import os
import requests

from datetime import datetime
from parser_tools.parser import Parser
from utility.config import DATE_FORMAT


class Client:
    """
    Web client, based on requests
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Client, cls).__new__(cls)

        return cls.instance

    def __init__(self, currencies: str = None, date: str = None):
        self.base_url = 'http://www.cbr.ru'
        self.base_path = os.path.relpath(os.path.expanduser('../Currencies/curr_base.html'))
        self.currencies = currencies

        if date and not Parser.check_date(date=date):
            raise ValueError(f'Invalid date format in "{date}"')

        if date and datetime.strptime(date, DATE_FORMAT) > datetime.now():
            raise ValueError('Incorrect date. Choose today or earlier')

        self.date = date

    def get_curr_base(self) -> str:
        """
        Get currency data from url
        :return: html code of page: str
        """

        url = f'{self.base_url}/currency_base/daily/'
        if self.date:
            url = f'{url}?UniDbQuery.Posted=True&UniDbQuery.To={self.date}'

        resp = requests.get(url=url)

        return Parser(text=resp.text, currencies=self.currencies).get_curr_info()

    def get_curr_from_file(self) -> str:
        """
        Get currency data from html file
        :return: html code of page: str
        """

        if not os.path.exists(self.base_path):
            raise FileNotFoundError(f'Currency HTML file "{self.base_path}" does not exist')

        with open(self.base_path, 'r', encoding='utf-8') as f:
            text = f.read()

            return Parser(text=text, currencies=self.currencies).get_curr_info()
