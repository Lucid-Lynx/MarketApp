import numpy as np

from numpy import ndarray
from decimal import Decimal
from stats.stats import Stats
from stats.numpy_stats.numpy_storage import StorageNumpy


class StatsNumpy(Stats):
    """
    Class, for statistics operations via Numpy
    """

    def __init__(self):
        self.storage = StorageNumpy()

    def sma(self, n: int = 1) -> list:
        """
        Compute simple moving average (SMA)
        :param n: Window size: int
        :return: List with SMAs from all windows: list
        """

        sma = []
        for i in range(len(self.storage.data[:, 1]) - n + 1):
            sma.append(sum(self.storage.data[i:i+n, 1])/n)

        return sma

    def average(self) -> (ndarray, Decimal):
        """
        Get average value of rates
        :return: average value: ndarray, Decimal
        """

        return np.mean(self.storage.data[:, 1])

    def min(self) -> (ndarray, Decimal):
        """
        Get minimal value of rates
        :return: minimal value: ndarray, Decimal
        """

        return np.amin(self.storage.data[:, 1])

    def max(self) -> (ndarray, Decimal):
        """
        Get maximum value of rates
        :return: maximum value: ndarray, Decimal
        """

        return np.amax(self.storage.data[:, 1])
