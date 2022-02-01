import tkinter.tix
from decimal import Decimal
from utility.config import DEFAULT_BASE_CURRENCY


class Currency:
    """
    Currency data structure
    """

    def __init__(
            self, code: str = DEFAULT_BASE_CURRENCY, base_currency: str = DEFAULT_BASE_CURRENCY, quantity: int = 1,
            rate: (int, Decimal) = 1):
        self.code = code
        self.__base_currency = base_currency
        self.__quantity = quantity
        self.__rate = Decimal(rate)

        self.__rate_conversion()

    @property
    def base_currency(self) -> str:
        return self.__base_currency

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def rate(self) -> (int, Decimal):
        return self.__rate

    def __rate_conversion(self):
        """
        Get base rate for 1 base currency unit
        :return: None
        """

        if self.quantity > 1:
            self.__rate = self.rate / self.quantity
            self.__quantity = 1
