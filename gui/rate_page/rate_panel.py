import wx
import wx.adv
import logging

from utility.config import DATE_FORMAT
from gui.loading_dialog import load_process
from gui.panel import Panel, handle_exception
from gui.rate_page import PAGE_NAME
from gui.rate_page.rate_view import RateView

logging.basicConfig(level=logging.INFO)


class RatePanel(Panel):

    def __init__(self, parent, name=PAGE_NAME):
        super().__init__(parent, name=name)

        self.view = RateView()

        self.label_mode = wx.StaticText(self, label='Mode', pos=(10, 95))
        self.choice_mode = wx.Choice(self, choices=['Remote', 'File'], pos=(140, 90))
        self.choice_mode.Bind(wx.EVT_CHOICE, self.__on_choice_mode)
        self.choice_mode.SetSelection(0)

        self.label_date = wx.StaticText(self, label='Date', pos=(10, 135))
        self.calendar_date = wx.adv.CalendarCtrl(self, pos=(140, 130))
        self.calendar_date.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.__on_choice_date)

        self.button_rate = wx.Button(self, label='Get rate', pos=(10, 175))
        self.button_rate.Bind(wx.EVT_BUTTON, self.__on_button_get_rate)

        self.label_rate = wx.StaticText(self, label='Rate', pos=(10, 315))
        self.rate_value = wx.StaticText(self, pos=(130, 355))

        self._update_data()

    @load_process
    def _collect_data(self):
        self.view.get_data(target_date=self.view.target_date)
        self._update_view()

    def _update_view(self):
        super()._update_view()
        self.__update_date_view()
        self.__update_mode_view()

    def __update_mode_view(self):
        self.view.mode = self.choice_mode.GetStringSelection()

    @handle_exception
    def __update_date_view(self):
        new_date = self.calendar_date.GetDate().Format(format=DATE_FORMAT)

        if new_date != self.view.target_date:
            self.view.target_date = new_date
            self._update_data()

        self.calendar_date.SetDateRange(upperdate=wx.DateTime.Today())

    def _update_base_cur_checkbox(self):
        self.choice_base_cur.Clear()
        self.choice_base_cur.AppendItems(self.view.get_available_bases(target_date=self.view.target_date))

    def _update_target_cur_checkbox(self):
        self.choice_target_cur.Clear()
        self.choice_target_cur.AppendItems(self.view.get_available_targets(target_date=self.view.target_date))

    def __on_choice_mode(self, event):
        self.__update_mode_view()

    def __on_choice_date(self, event):
        self.__update_date_view()

    def __on_button_get_rate(self, event):
        self.view.get_rate()

        if self.view.rate:
            self.rate_value.SetLabel(label=str(self.view.rate))
        else:
            self.rate_value.SetLabel(label='')
