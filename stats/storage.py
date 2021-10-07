import numpy as np
import logging
from decimal import Decimal
from datetime import date

logging.basicConfig(level=logging.INFO)


class Storage:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance

    def __init__(self, values=None):
        if not len(self.__dict__):
            self.values = values if values is not None else np.zeros((1, 2), dtype=Decimal)

    def add_value(self, value, current_date=date.today().toordinal()):
        self.values = np.append(self.values, [[current_date, value]], axis=0)

    def clean(self):
        self.values = self.values[:1]
