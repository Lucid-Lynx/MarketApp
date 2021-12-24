import logging
import numpy as np

from stats.stats import Stats
from stats.numpy_stats.numpy_storage import StorageNumpy

logging.basicConfig(level=logging.INFO)


class StatsNumpy(Stats):

    def __init__(self):
        self.storage = StorageNumpy()

    def sma(self):
        return np.average(self.storage.data, axis=0)[1]

    def min(self):
        return np.amin(self.storage.data, axis=0)[1]

    def max(self):
        return np.amax(self.storage.data, axis=0)[1]
