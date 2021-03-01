import aiohttp
import logging
from parser.parser import Parser

logging.basicConfig(level=logging.INFO)


class Client:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Client, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.base_url = 'http://www.cbr.ru'

    async def get_cur_base(self, numeric=None, alpha=None):
        url = f'{self.base_url}/currency_base/daily/'

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as resp:
                text = await resp.text()
                return Parser(text=text).get_curr_info(numeric=numeric, alpha=alpha)
