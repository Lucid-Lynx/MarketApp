from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Abstract class for stats storage
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance

    def __init__(self, values: dict = None):
        if not len(self.__dict__):
            self.values = values if values else []
            self.data = self.values

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, values: dict):
        self.__data = values

    @abstractmethod
    def add_value(self, *args, **kwargs):
        pass

    def clean(self):
        """
        Clean storage
        :return: None
        """

        self.values = []
        self.update_data()

    def update_data(self):
        """
        Update data in storage
        :return:
        """

        self.data = self.values
