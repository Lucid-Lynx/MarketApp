import wx
import wx.adv
import logging

from gui.loading_dialog import load_process
from gui.numpy_page.numpy_panel import NumpyPanel
from gui.pandas_page import PAGE_NAME
from gui.pandas_page.pandas_view import PandasView
from stats.pandas_stats.pandas_stats import StatsPandas

logging.basicConfig(level=logging.INFO)


class PandasPanel(NumpyPanel):

    def __init__(self, parent, name=PAGE_NAME):
        super().__init__(parent, name=name)

        self.view = PandasView()

        self.button_save_rate = wx.Button(self, label='Show charts', pos=(10, 175))
        self.button_save_rate.Bind(wx.EVT_BUTTON, self.__on_button_show_charts)

        self._update_data()

    @load_process
    def _get_stats(self):
        self.view.save_rates()
        self.view.sma = StatsPandas().sma()
        self.view.min = StatsPandas().min()
        self.view.max = StatsPandas().max()

    def __on_button_show_charts(self, event):
        pass
