import pandas as pd

from decimal import Decimal
from datetime import date
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from stats.storage import Storage


class StoragePandas(Storage):
    """
    Storage for Pandas statistics
    """

    def __init__(self, values: dict = None):
        super().__init__(values=values)

    @Storage.data.setter
    def data(self, values: dict):
        Storage.data.fset(self, pd.DataFrame({
            'Date': list(map(lambda x: pd.to_datetime(x['date'], format=DATE_FORMAT), values)),
            'Base Currency': list(map(lambda x: x['base_currency'], values)),
            'Target Currency': list(map(lambda x: x['target_currency'], values)),
            'Rate': list(map(lambda x: x['rate'], values)),
        }))

    def add_value(
            self, value: Decimal, current_date: date = date.today(), base_currency: str = DEFAULT_BASE_CURRENCY,
            target_currency: str = DEFAULT_BASE_CURRENCY):
        """
        Add new data into storage
        :param value: Currency rate: Decimal
        :param current_date: Current date: date
        :param base_currency: Base currency: str
        :param target_currency: Target currency: str
        :return: None
        """

        self.values.append({
            'date': current_date,
            'base_currency': base_currency,
            'target_currency': target_currency,
            'rate': value,
        })
