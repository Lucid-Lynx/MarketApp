import numpy as np

from decimal import Decimal
from datetime import date
from stats.storage import Storage


class StorageNumpy(Storage):
    """
    Storage for Numpy statistics
    """

    def __init__(self, values: dict = None):
        # super().__init__(values if values is not None else np.zeros((1, 2), dtype=Decimal))
        super().__init__(values=values)

    @Storage.data.setter
    def data(self, values: dict):
        Storage.data.fset(
            self, np.zeros((1, 2), dtype=Decimal) if not len(values)
            else np.array(list(map(lambda x: [x['date'], x['rate']], values))))

    def add_value(self, value: Decimal, current_date: date = date.today()):
        """
        Add new data into storage
        :param value: Currency rate: Decimal
        :param current_date: Current date: date
        :return: None
        """

        # self.values = np.append(self.values, [[current_date, value]], axis=0)

        self.values.append({
            'date': current_date,
            'rate': value,
        })
