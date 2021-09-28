import logging

from datetime import date, datetime, timedelta
from stats.storage import Storage
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from gui.view import View

logging.basicConfig(level=logging.INFO)


class StatsView(View):

    def __init__(
            self, base_cur=DEFAULT_BASE_CURRENCY, target_cur=DEFAULT_BASE_CURRENCY,
            from_date=date.today().strftime(DATE_FORMAT), to_date=date.today().strftime(DATE_FORMAT)):

        super().__init__(base_cur=base_cur, target_cur=target_cur)

        self.sma = 0
        self.__from_date = from_date
        self.__to_date = to_date
        self.__storage = Storage()

    @property
    def from_date(self):
        return self.__from_date

    @from_date.setter
    def from_date(self, from_date):
        self.__from_date = from_date
        self.check_dates()

    @property
    def to_date(self):
        return self.__to_date

    @to_date.setter
    def to_date(self, to_date):
        self.__to_date = to_date
        self.check_dates()

    @property
    def storage(self):
        return self.__storage

    def check_dates(self):
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

    def save_rates(self):
        self.storage.clean()
        from_date_obj = datetime.strptime(self.from_date, DATE_FORMAT)
        to_date_obj = datetime.strptime(self.to_date, DATE_FORMAT)

        while from_date_obj <= to_date_obj:
            self.storage.add_value(
                value=self.get_rate(target_date=from_date_obj.strftime(DATE_FORMAT)),
                current_date=from_date_obj.toordinal())
            from_date_obj = from_date_obj + timedelta(days=1)

    def __get_date_range(self):
        date_range = []
        from_date_obj = datetime.strptime(self.from_date, DATE_FORMAT)
        to_date_obj = datetime.strptime(self.to_date, DATE_FORMAT)

        while from_date_obj <= to_date_obj:
            date_range.append(from_date_obj)
            from_date_obj = from_date_obj + timedelta(days=1)

        return date_range
