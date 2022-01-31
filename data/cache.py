from datetime import date, datetime
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from .record import Record


class Cache:
    """
    Class for cache
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Cache, cls).__new__(cls)

        return cls.instance

    def __init__(self, data: list = None, base_currency: str = DEFAULT_BASE_CURRENCY):
        if not hasattr(self, 'data'):
            self.data = data or []

        self.base_currency = base_currency

    def get_record(self, current_date: str = date.today().strftime(DATE_FORMAT)) -> Record:
        """
        Get record from cache
        :param current_date: current date: str
        :return: found record: Record
        """

        found = list(filter(lambda x: x.current_date == current_date, self.data))

        return found[0] if len(found) else None

    def add_record(self, record: Record):
        """
        Add record into cache
        :param record: new record: Record
        :return: None
        """

        found = self.get_record(current_date=record.current_date)

        if not found:
            self.data.append(record)
            self.__sort()

    def remove_record(self, current_date: str = date.today().strftime(DATE_FORMAT)):
        """
        Remove record from cache
        :param current_date: current date: str
        :return: None
        """

        found = self.get_record(current_date=current_date)
        self.data.remove(found)

    def clean(self):
        """
        Clean cache
        :return: None
        """

        self.data.clear()

    def __sort(self):
        """
        Sort data in cache
        :return: None
        """

        self.data.sort(key=self.__sorter)

    @staticmethod
    def __sorter(record: Record):
        """
        Sorter by date
        :param record: record: Record
        :return: date: str
        """

        return datetime.strptime(record.current_date, DATE_FORMAT)
