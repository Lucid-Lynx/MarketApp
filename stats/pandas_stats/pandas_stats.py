from decimal import Decimal
from stats.stats import Stats
from stats.pandas_stats.pandas_storage import StoragePandas


class StatsPandas(Stats):
    """
    Class, for statistics operations via Pandas
    """

    def __init__(self):
        self.storage = StoragePandas()

    def sma(self, n: int = 1) -> list:
        """
        Compute simple moving average (SMA)
        :param n: Window size: int
        :return: List with SMAs from all windows: list
        """

        sma = []
        for i in range(len(self.storage.data['Rate']) - n + 1):
            sma.append(sum(self.storage.data['Rate'][i:i + n]) / n)

        return sma

    def average(self) -> Decimal:
        """
        Get average value of rates
        :return: average value: Decimal
        """

        return self.storage.data['Rate'].mean()

    def min(self):
        """
        Get minimal value of rates
        :return: minimal value: Decimal
        """

        return self.storage.data['Rate'].min()

    def max(self):
        """
        Get maximum value of rates
        :return: maximum value: Decimal
        """

        return self.storage.data['Rate'].max()
