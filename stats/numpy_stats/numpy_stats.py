import numpy as np

from stats.stats import Stats
from stats.numpy_stats.numpy_storage import StorageNumpy


class StatsNumpy(Stats):

    def __init__(self):
        self.storage = StorageNumpy()

    def sma(self, n=1):
        sma = []
        for i in range(len(self.storage.data[:, 1]) - n + 1):
            sma.append(sum(self.storage.data[i:i+n, 1])/n)

        return sma

    def average(self):
        return np.mean(self.storage.data[:, 1])

    def min(self):
        return np.amin(self.storage.data[:, 1])

    def max(self):
        return np.amax(self.storage.data[:, 1])
