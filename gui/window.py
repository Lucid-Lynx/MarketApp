import wx
import wx.adv
import logging

from gui.rate_page.rate_panel import RatePanel, PAGE_NAME as RATES_PAGE_NAME
from gui.stats_page.stats_panel import StatsPanel, PAGE_NAME as STATS_PAGE_NAME

logging.basicConfig(level=logging.INFO)


class Window(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 500))

        self.nb = wx.Notebook(self)
        self.nb.AddPage(page=RatePanel(self.nb), text=RATES_PAGE_NAME)
        self.nb.AddPage(page=StatsPanel(self.nb), text=STATS_PAGE_NAME)

        self.Center()
        self.Show(True)
