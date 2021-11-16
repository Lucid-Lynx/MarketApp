import logging

from datetime import date, datetime
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from gui.view import View

logging.basicConfig(level=logging.INFO)


class RateView(View):

    def __init__(
            self, base_cur=DEFAULT_BASE_CURRENCY, target_cur=DEFAULT_BASE_CURRENCY,
            target_date=date.today().strftime(DATE_FORMAT), mode='Remote'):

        super().__init__(base_cur=base_cur, target_cur=target_cur, mode=mode)

        self.__target_date = target_date
        self.__rate = 0

    @property
    def target_date(self):
        return self.__target_date

    @target_date.setter
    def target_date(self, target_date):
        self.__target_date = target_date
        self.check_dates()

    @property
    def rate(self):
        return self.__rate

    def get_rate(self, target_date=date.today().strftime(DATE_FORMAT)):
        self.__rate = super().get_rate(target_date=self.target_date)

        return self.__rate

    def get_available_bases(self, target_date=date.today().strftime(DATE_FORMAT)):
        return super().get_available_bases(target_date=self.target_date)

    def get_available_targets(self, target_date=date.today().strftime(DATE_FORMAT)):
        return super().get_available_targets(target_date=self.target_date)

    def check_dates(self):
        if datetime.strptime(self.target_date, DATE_FORMAT) > datetime.now():
            err = 'Invalid target date. Choose today or earlier'
            logging.error(err)
            raise ValueError(err)

    '''
    def get_rate(self):
        if self.mode == 'File':
            resp = Client(currencies=self.target_cur).get_curr_from_file()
        else:
            resp = Client(currencies=self.target_cur, date=self.target_date).get_curr_base()

        logging.info(resp)
        self.rate = resp['currencies'][self.target_cur]['base_value']
    '''
