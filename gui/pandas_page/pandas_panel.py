import wx
import wx.adv
import matplotlib
import matplotlib.pyplot as plt

from utility.config import DATE_FORMAT
from matplotlib.dates import DateFormatter, DayLocator
from gui.panel import handle_exception
from gui.numpy_page.numpy_panel import NumpyPanel
from gui.pandas_page import PAGE_NAME
from gui.pandas_page.pandas_view import PandasView
from stats.pandas_stats.pandas_stats import StatsPandas
from stats.pandas_stats.pandas_storage import StoragePandas

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class PandasPanel(NumpyPanel):
    """
    Panel for Pandas page
    """

    def __init__(self, parent: wx.Window, name: str = PAGE_NAME):
        super().__init__(parent, name=name)

        self.view = PandasView()

        self.button_save_rate = wx.Button(self, label='Show charts', pos=(10, 175))
        self.button_save_rate.Bind(wx.EVT_BUTTON, self.__on_button_show_charts)

        self.plot_panel = PlotPanel(parent=self, size=(700, 700), pos=(800, 10))

        self._update_data()

    @handle_exception
    def _get_stats(self):
        """
        Compute all statistic metrics
        :return: None
        """

        self.view.save_rates()
        self.view.check_window_size()
        self.view.sma = StatsPandas().sma(n=self.view.win_size)
        self.view.average = StatsPandas().average()
        self.view.min = StatsPandas().min()
        self.view.max = StatsPandas().max()

    def __on_button_show_charts(self, event: wx.Event):
        """
        Callback for show charts button
        :param event: generated event: Event
        :return: None
        """

        self._on_button_get_stats(event)
        self.plot_panel.draw()


class PlotPanel(wx.Panel):
    """
    Panel for plots
    """

    def __init__(self, parent: wx.Window, size: tuple, pos: tuple = (0, 0)):
        wx.Panel.__init__(self, parent=parent, size=size, pos=pos)

        self.__storage = StoragePandas()

        self.figure, self.axes = plt.subplots(1, 1)
        self.figure.set_figwidth(7)
        self.figure.set_figheight(7)

        self.canvas = FigureCanvas(self, -1, self.figure)

    @property
    def storage(self) -> StoragePandas:
        return self.__storage

    def draw(self):
        """
        Draw plot for data from storage
        :return: None
        """

        self.axes.clear()

        dates = self.storage.data['Date'].tolist()
        rates = self.storage.data['Rate'].tolist()

        self.axes.xaxis.set_major_locator(DayLocator())
        self.axes.xaxis.set_major_formatter(DateFormatter(DATE_FORMAT))
        self.axes.fmt_xdata = DateFormatter(DATE_FORMAT)

        plt.xticks(rotation=45)

        self.axes.plot(dates, rates)
        plt.scatter(dates, rates, s=10)

        plt.locator_params(axis='x', nbins=len(dates))
        plt.locator_params(axis='y', nbins=len(rates))
        plt.draw()
