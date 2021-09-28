import logging
from decimal import Decimal
from stats.storage import Storage

logging.basicConfig(level=logging.INFO)


class Stats:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Stats, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.storage = Storage()

    def sma(self):
        arr = [x['value'] for x in self.storage.values]
        return sum(arr) / Decimal(len(arr))
