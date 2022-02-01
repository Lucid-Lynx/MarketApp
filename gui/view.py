from decimal import Decimal
from datetime import date
from web.client import Client
from data.cache import Cache
from data.record import Record
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from gui.loading_dialog import load_process


class View:
    """
    Base view, which provides current state of GUI page
    """

    def __init__(
            self, base_cur: str = DEFAULT_BASE_CURRENCY, target_cur: str = DEFAULT_BASE_CURRENCY,
            mode: str = 'Remote'):
        self.base_cur = base_cur
        self.target_cur = target_cur
        self.mode = mode
        self.__store = Cache()

    @property
    def store(self) -> Cache:
        return self.__store

    def clean_store(self):
        """
        Clean cache
        :return: None
        """

        self.store.clean()
        self.store.add_record(Record(data=self.load_rates()))

    @load_process
    def update_store(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> Record:
        """
        Update cache, add new record
        :param target_date: target date for data to store: str
        :return: new record: Record
        """

        record = Record(data=self.load_rates(target_date=target_date), current_date=target_date)
        self.store.add_record(record=record)

        return record

    def get_data(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> Record:
        """
        Get record from cache by date
        :param target_date: target date for data to store: str
        :return: new record: Record
        """

        record = self.store.get_record(current_date=target_date)

        return record or self.update_store(target_date=target_date)

    def load_rates(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> str:
        """
        Load new data with rates from remote source or file
        :param target_date: target date: str
        :return: text response: str
        """

        if self.mode == 'Remote':
            resp = Client(date=target_date).get_curr_base()
        else:
            resp = Client().get_curr_from_file()

        return resp

    def get_rate(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> (int, Decimal):
        """
        Get rate data from cache
        :param target_date: target date: str
        :return: currency rate: int, Decimal
        """

        record = self.get_data(target_date=target_date)

        if not record:
            return 0

        base_rate_data = record.rates.get(self.base_cur)
        target_rate_data = record.rates.get(self.target_cur)
        return target_rate_data.rate / base_rate_data.rate if base_rate_data and target_rate_data else 0

    def get_available_bases(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> list:
        """
        Get list with available base currencies
        :param target_date: target date: str
        :return: list with base currencies: list
        """

        record = self.store.get_record(current_date=target_date)

        return record.available_currencies if record else [DEFAULT_BASE_CURRENCY]

    def get_available_targets(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> list:
        """
        Get list with available target currencies
        :param target_date: target date: str
        :return: list with target currencies: list
        """

        available_bases = self.get_available_bases(target_date=target_date)

        if len(available_bases):
            available_targets = available_bases.copy()
            available_targets.remove(self.base_cur)

            return available_targets if len(available_targets) else [DEFAULT_BASE_CURRENCY]

        else:
            return [DEFAULT_BASE_CURRENCY]

    def check_dates(self):
        """
        Base method for checking dates
        :return: None
        """

        pass
