from abc import ABC, abstractmethod


class Stats(ABC):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Stats, cls).__new__(cls)
        return cls.instance

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def sma(self):
        pass

    @abstractmethod
    def min(self):
        pass

    @abstractmethod
    def max(self):
        pass
