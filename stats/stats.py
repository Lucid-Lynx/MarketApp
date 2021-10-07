import logging
import numpy as np
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
        return np.average(self.storage.values[1:], axis=0)[1]

    def min(self):
        return np.amin(self.storage.values[1:], axis=0)[1]

    def max(self):
        return np.amax(self.storage.values[1:], axis=0)[1]
