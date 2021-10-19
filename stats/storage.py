import logging

from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


class Storage(ABC):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance

    def __init__(self, values=None):
        if not len(self.__dict__):
            self.values = values if values else []
            self.data = self.values

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, values):
        self.__data = values

    @abstractmethod
    def add_value(self, *args, **kwargs):
        pass

    def clean(self):
        self.values = []
        self.update_data()

    def update_data(self):
        self.data = self.values
