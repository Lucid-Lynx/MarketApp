from stats.stats import Stats
from stats.pandas_stats.pandas_storage import StoragePandas


class StatsPandas(Stats):

    def __init__(self):
        self.storage = StoragePandas()

    def sma(self, n=1):
        sma = []
        for i in range(len(self.storage.data['Rate']) - n + 1):
            sma.append(sum(self.storage.data['Rate'][i:i + n]) / n)

        return sma

    def average(self):
        return self.storage.data['Rate'].mean()

    def min(self):
        return self.storage.data['Rate'].min()

    def max(self):
        return self.storage.data['Rate'].max()
