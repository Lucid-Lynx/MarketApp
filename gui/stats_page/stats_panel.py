import wx
import wx.adv
import logging

from utility.config import DATE_FORMAT
from stats.stats import Stats
from gui.loading_dialog import load_process
from gui.panel import Panel, handle_exception
from gui.stats_page import PAGE_NAME
from gui.stats_page.stats_view import StatsView

logging.basicConfig(level=logging.INFO)


class StatsPanel(Panel):

    def __init__(self, parent, name=PAGE_NAME):
        super().__init__(parent, name=name)

        self.view = StatsView()

        self.label_from_date = wx.StaticText(self, label='From', pos=(10, 95))
        self.calendar_from_date = wx.adv.CalendarCtrl(self, pos=(140, 90))
        self.calendar_from_date.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.__on_choice_from_date)

        self.label_to_date = wx.StaticText(self, label='To', pos=(390, 95))
        self.calendar_to_date = wx.adv.CalendarCtrl(self, pos=(520, 90))
        self.calendar_to_date.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.__on_choice_to_date)

        self.button_save_rate = wx.Button(self, label='Get stats', pos=(10, 135))
        self.button_save_rate.Bind(wx.EVT_BUTTON, self.__on_button_get_stats)

        self.label_sma = wx.StaticText(self, label='SMA', pos=(10, 275))
        self.sma_value = wx.StaticText(self, pos=(140, 270))

        self.label_min = wx.StaticText(self, label='Min', pos=(10, 315))
        self.min_value = wx.StaticText(self, pos=(140, 310))

        self.label_max = wx.StaticText(self, label='Max', pos=(10, 355))
        self.max_value = wx.StaticText(self, pos=(140, 350))

        self._update_data()

    @load_process
    def __get_stats(self):
        self.view.save_rates()
        self.view.sma = Stats().sma()
        self.view.min = Stats().min()
        self.view.max = Stats().max()

    def _update_view(self):
        super()._update_view()
        self.__update_from_date_view()
        self.__update_to_date_view()

    @handle_exception
    def __update_from_date_view(self):
        new_date = self.calendar_from_date.GetDate().Format(format=DATE_FORMAT)

        if new_date != self.view.from_date:
            self.view.from_date = new_date

        to_date_obj = wx.DateTime()
        to_date_obj.ParseFormat(self.view.to_date, DATE_FORMAT)
        self.calendar_from_date.SetDateRange(upperdate=to_date_obj)

    @handle_exception
    def __update_to_date_view(self):
        new_date = self.calendar_to_date.GetDate().Format(format=DATE_FORMAT)

        if new_date != self.view.to_date:
            self.view.to_date = new_date

        from_date_obj = wx.DateTime()
        from_date_obj.ParseFormat(self.view.from_date, DATE_FORMAT)
        self.calendar_to_date.SetDateRange(lowerdate=from_date_obj, upperdate=wx.DateTime.Today())

    def __on_choice_from_date(self, event):
        self.__update_from_date_view()

    def __on_choice_to_date(self, event):
        self.__update_to_date_view()

    def __on_button_get_stats(self, event):
        self.__get_stats()

        if self.view.sma:
            self.sma_value.SetLabel(label=str(self.view.sma))
        else:
            self.sma_value.SetLabel(label='')

        if self.view.min:
            self.min_value.SetLabel(label=str(self.view.min))
        else:
            self.min_value.SetLabel(label='')

        if self.view.max:
            self.max_value.SetLabel(label=str(self.view.max))
        else:
            self.max_value.SetLabel(label='')
