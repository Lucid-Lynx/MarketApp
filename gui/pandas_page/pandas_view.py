from datetime import date, datetime, timedelta
from stats.pandas_stats.pandas_storage import StoragePandas
from utility.config import DEFAULT_BASE_CURRENCY, DATE_FORMAT
from gui.numpy_page.numpy_view import NumpyView


class PandasView(NumpyView):
    """
    Pandas stats view, which provides current state of Pandas stats page
    """

    def __init__(
            self, base_cur: str = DEFAULT_BASE_CURRENCY, target_cur: str = DEFAULT_BASE_CURRENCY,
            from_date: str = date.today().strftime(DATE_FORMAT), to_date: str = date.today().strftime(DATE_FORMAT)):

        super().__init__(base_cur=base_cur, target_cur=target_cur, from_date=from_date, to_date=to_date)
        self._storage = StoragePandas()

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
                value=self.get_rate(target_date=from_date_obj.strftime(DATE_FORMAT)),
                current_date=from_date_obj.strftime(DATE_FORMAT), base_currency=self.base_cur,
                target_currency=self.target_cur)
            from_date_obj = from_date_obj + timedelta(days=1)

        self.storage.update_data()
