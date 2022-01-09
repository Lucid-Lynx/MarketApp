import pandas as pd

from datetime import date
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from stats.storage import Storage


class StoragePandas(Storage):

    def __init__(self, values=None):
        super().__init__(values=values)

    @Storage.data.setter
    def data(self, values):
        Storage.data.fset(self, pd.DataFrame({
            'Date': list(map(lambda x: pd.to_datetime(x['date'], format=DATE_FORMAT), values)),
            'Base Currency': list(map(lambda x: x['base_currency'], values)),
            'Target Currency': list(map(lambda x: x['target_currency'], values)),
            'Rate': list(map(lambda x: x['rate'], values)),
        }))

    def add_value(
            self, value, current_date=date.today(), base_currency=DEFAULT_BASE_CURRENCY,
            target_currency=DEFAULT_BASE_CURRENCY):

        self.values.append({
            'date': current_date,
            'base_currency': base_currency,
            'target_currency': target_currency,
            'rate': value,
        })
