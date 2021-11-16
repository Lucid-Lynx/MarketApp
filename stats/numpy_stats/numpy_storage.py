import numpy as np
import logging

from decimal import Decimal
from datetime import date
from stats.storage import Storage

logging.basicConfig(level=logging.INFO)


class StorageNumpy(Storage):

    def __init__(self, values=None):
        # super().__init__(values if values is not None else np.zeros((1, 2), dtype=Decimal))
        super().__init__(values=values)

    @Storage.data.setter
    def data(self, values):
        Storage.data.fset(
            self, np.zeros((1, 2), dtype=Decimal) if not len(values)
            else np.array(list(map(lambda x: [x['date'], x['rate']], values))))

    def add_value(self, value, current_date=date.today().toordinal()):
        # self.values = np.append(self.values, [[current_date, value]], axis=0)

        self.values.append({
            'date': current_date,
            'rate': value,
        })
