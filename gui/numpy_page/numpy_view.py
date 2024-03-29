import logging

from datetime import date, datetime, timedelta
from stats.numpy_stats.numpy_storage import StorageNumpy
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from gui.view import View

logging.basicConfig(level=logging.INFO)


class NumpyView(View):
    """
    Numpy stats view, which provides current state of Numpy stats page
    """

    def __init__(
            self, base_cur: str = DEFAULT_BASE_CURRENCY, target_cur: str = DEFAULT_BASE_CURRENCY,
            from_date: str = date.today().strftime(DATE_FORMAT), to_date: str = date.today().strftime(DATE_FORMAT)):

        super().__init__(base_cur=base_cur, target_cur=target_cur)

        self.win_size = 1
        self.sma = []
        self.average = 0
        self.min = 0
        self.max = 0
        self.__from_date = from_date
        self.__to_date = to_date
        self._storage = StorageNumpy()

    @property
    def from_date(self) -> str:
        return self.__from_date

    @from_date.setter
    def from_date(self, from_date: str):
        self.__from_date = from_date
        self.check_dates()

    @property
    def to_date(self) -> str:
        return self.__to_date

    @to_date.setter
    def to_date(self, to_date: str):
        self.__to_date = to_date
        self.check_dates()

    @property
    def storage(self) -> StorageNumpy:
        return self._storage

    def check_dates(self):
        """
       Check base and target dates for validity
       :raises: ValueError
       :return: None
       """

        from_date_obj = datetime.strptime(self.from_date, DATE_FORMAT)
        to_date_obj = datetime.strptime(self.to_date, DATE_FORMAT)

        if from_date_obj > datetime.now():
            err = 'Invalid from date. Choose today or earlier'
            logging.error(err)
            raise ValueError(err)

        if to_date_obj > datetime.now():
            err = 'Invalid to date. Choose today or earlier'
            logging.error(err)
            raise ValueError(err)

        if from_date_obj > to_date_obj:
            err = 'Invalid dates. From date should be equal or earlier than to date'
            logging.error(err)
            raise ValueError(err)

    def check_window_size(self):
        """
        Check window size with current data records quantity inside local storage
        :raises: ValueError
        :return: None
        """

        if self.win_size > len(self.storage.data):
            err = 'Window size is higher, than collected data quantity!'
            logging.error(err)
            raise ValueError(err)

    def save_rates(self):
        """
        Save rates into local storage for statistics
        :return: None
        """

        self.storage.clean()
        from_date_obj = datetime.strptime(self.from_date, DATE_FORMAT)
        to_date_obj = datetime.strptime(self.to_date, DATE_FORMAT)

        while from_date_obj <= to_date_obj:
            self.storage.add_value(
                value=self.get_rate(target_date=from_date_obj.strftime(DATE_FORMAT)), current_date=from_date_obj)
            from_date_obj = from_date_obj + timedelta(days=1)

        self.storage.update_data()

    def __get_date_range(self) -> list:
        """
        Get list with date range
        :return: list
        """

        date_range = []
        from_date_obj = datetime.strptime(self.from_date, DATE_FORMAT)
        to_date_obj = datetime.strptime(self.to_date, DATE_FORMAT)

        while from_date_obj <= to_date_obj:
            date_range.append(from_date_obj)
            from_date_obj = from_date_obj + timedelta(days=1)

        return date_range
