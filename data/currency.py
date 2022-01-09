from decimal import Decimal
from utility.config import DEFAULT_BASE_CURRENCY


class Currency:

    def __init__(
            self, code=DEFAULT_BASE_CURRENCY, base_currency=DEFAULT_BASE_CURRENCY, quantity=1, rate=1):
        self.code = code
        self.__base_currency = base_currency
        self.__quantity = quantity
        self.__rate = Decimal(rate)

        self.__rate_conversion()

    @property
    def base_currency(self):
        return self.__base_currency

    @property
    def quantity(self):
        return self.__quantity

    @property
    def rate(self):
        return self.__rate

    def __rate_conversion(self):
        if self.quantity > 1:
            self.__rate = self.rate / self.quantity
            self.__quantity = 1

    def change_base_currency(self, base_currency=DEFAULT_BASE_CURRENCY, base_rate=1):
        self.__base_currency = base_currency
        self.__rate = self.rate / base_rate

    def update_data(self, base_currency=DEFAULT_BASE_CURRENCY, quantity=1, rate=1):
        self.__init__(code=self.code, base_currency=base_currency, quantity=quantity, rate=rate)
