from stats.stats import Stats
from stats.pandas_stats.pandas_storage import StoragePandas


class StatsPandas(Stats):

    def __init__(self):
        self.storage = StoragePandas()

    def sma(self):
        return self.storage.data['Rate'].mean()

    def min(self):
        return self.storage.data['Rate'].min()

    def max(self):
        return self.storage.data['Rate'].max()
