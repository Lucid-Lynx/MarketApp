import logging

from datetime import date, datetime
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from .record import Record

logging.basicConfig(level=logging.INFO)


class Cache:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Cache, cls).__new__(cls)

        return cls.instance

    def __init__(self, data=None, base_currency=DEFAULT_BASE_CURRENCY):
        if not hasattr(self, 'data'):
            self.data = data or []

        self.base_currency = base_currency

    def get_record(self, current_date=date.today().strftime(DATE_FORMAT)):
        found = list(filter(lambda x: x.current_date == current_date, self.data))

        return found[0] if len(found) else None

    def add_record(self, record: Record):
        found = self.get_record(current_date=record.current_date)

        if not found:
            self.data.append(record)
            self.__sort()

    def remove_record(self, current_date=date.today().strftime(DATE_FORMAT)):
        found = self.get_record(current_date=current_date)
        self.data.remove(found)

    def clean(self):
        self.data.clear()

    def __sort(self):
        self.data.sort(key=self.__sorter)

    @staticmethod
    def __sorter(record: Record):
        return datetime.strptime(record.current_date, DATE_FORMAT)
