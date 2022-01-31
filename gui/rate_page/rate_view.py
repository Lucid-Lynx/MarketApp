import logging

from decimal import Decimal
from datetime import date, datetime
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from gui.view import View

logging.basicConfig(level=logging.INFO)


class RateView(View):
    """
    Rate view, which provides current state of rate page
    """

    def __init__(
            self, base_cur: str = DEFAULT_BASE_CURRENCY, target_cur: str = DEFAULT_BASE_CURRENCY,
            target_date: str = date.today().strftime(DATE_FORMAT), mode: str = 'Remote'):

        super().__init__(base_cur=base_cur, target_cur=target_cur, mode=mode)

        self.__target_date = target_date
        self.__rate = 0

    @property
    def target_date(self) -> str:
        return self.__target_date

    @target_date.setter
    def target_date(self, target_date: str):
        self.__target_date = target_date
        self.check_dates()

    @property
    def rate(self) -> (int, Decimal):
        return self.__rate

    def get_rate(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> (int, Decimal):
        """
        Get rate for target date
        :param target_date: target date: str
        :return: current rate for target date
        """

        self.__rate = super().get_rate(target_date=self.target_date)

        return self.__rate

    def get_available_bases(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> list:
        """
        Get list with available base currencies
        :param target_date: target date: str
        :return: list with base currencies: list
        """

        return super().get_available_bases(target_date=self.target_date)

    def get_available_targets(self, target_date: str = date.today().strftime(DATE_FORMAT)) -> list:
        """
        Get list with available target currencies
        :param target_date: target date: str
        :return: list with target currencies: list
        """

        return super().get_available_targets(target_date=self.target_date)

    def check_dates(self):
        """
        Check target date for validity
        :raises: ValueError
        :return: None
        """

        if datetime.strptime(self.target_date, DATE_FORMAT) > datetime.now():
            err = 'Invalid target date. Choose today or earlier'
            logging.error(err)
            raise ValueError(err)

    '''
    def get_rate(self):
        """
        Get rate for target date
        :param target_date: target date: str 
        :return: None
        """
    
        if self.mode == 'File':
            resp = Client(currencies=self.target_cur).get_curr_from_file()
        else:
            resp = Client(currencies=self.target_cur, date=self.target_date).get_curr_base()

        logging.info(resp)
        self.rate = resp['currencies'][self.target_cur]['base_value']
    '''
