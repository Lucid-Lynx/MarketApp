import wx
import wx.adv

from gui.rate_page.rate_panel import RatePanel, PAGE_NAME as RATES_PAGE_NAME


class Window(wx.Frame):
    """
    Base window of GUI
    """

    def __init__(self, parent: wx.Window, title: str):
        super().__init__(parent, title=title)

        self.nb = wx.Notebook(self)
        self.nb.AddPage(page=RatePanel(self.nb), text=RATES_PAGE_NAME)

        self.Center()
        self.Show(True)
        self.Maximize(True)
