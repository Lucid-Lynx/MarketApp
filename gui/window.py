import wx
import wx.adv

from gui.rate_page.rate_panel import RatePanel, PAGE_NAME as RATES_PAGE_NAME
from gui.numpy_page.numpy_panel import NumpyPanel, PAGE_NAME as NUMPY_PAGE_NAME
from gui.pandas_page.pandas_panel import PandasPanel, PAGE_NAME as PANDAS_PAGE_NAME


class Window(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        self.nb = wx.Notebook(self)
        self.nb.AddPage(page=RatePanel(self.nb), text=RATES_PAGE_NAME)
        self.nb.AddPage(page=NumpyPanel(self.nb), text=NUMPY_PAGE_NAME)
        self.nb.AddPage(page=PandasPanel(self.nb), text=PANDAS_PAGE_NAME)

        self.Center()
        self.Show(True)
        self.Maximize(True)
