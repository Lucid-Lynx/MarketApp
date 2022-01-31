import wx
import wx.adv

from utility.config import DATE_FORMAT
from gui.panel import Panel, handle_exception
from gui.rate_page import PAGE_NAME
from gui.rate_page.rate_view import RateView


class RatePanel(Panel):
    """
    Panel for rate page
    """

    def __init__(self, parent: wx.Window, name: str = PAGE_NAME):
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
        self.rate_value = wx.StaticText(self, pos=(130, 310))

        self._update_data()

    def _collect_data(self):
        """
        Get current data from cache and set in the view
        :return: None
        """

        self.view.get_data(target_date=self.view.target_date)
        self._update_view()

    def _update_view(self):
        """
        Update view by data from panel
        :return: None
        """

        super()._update_view()
        self.__update_date_view()
        self.__update_mode_view()

    def __update_mode_view(self):
        """
        Update mode view
        :return: None
        """

        self.view.mode = self.choice_mode.GetStringSelection()

    @handle_exception
    def __update_date_view(self):
        """
        Update target date view
        :return: None
        """

        new_date = self.calendar_date.GetDate().Format(format=DATE_FORMAT)

        if new_date != self.view.target_date:
            self.view.target_date = new_date
            self._update_data()

        self.calendar_date.SetDateRange(upperdate=wx.DateTime.Today())

    def _update_base_cur_checkbox(self):
        """
        Update base currency checkbox
        :return: None
        """

        self.choice_base_cur.Clear()
        self.choice_base_cur.AppendItems(self.view.get_available_bases(target_date=self.view.target_date))

    def _update_target_cur_checkbox(self):
        """
        Update target currency checkbox
        :return: None
        """

        self.choice_target_cur.Clear()
        self.choice_target_cur.AppendItems(self.view.get_available_targets(target_date=self.view.target_date))

    def __on_choice_mode(self, event: wx.Event):
        """
        Callback for mode checkbox
        :param event: generated event: Event
        :return: None
        """

        self.__update_mode_view()

    def __on_choice_date(self, event: wx.Event):
        """
        Callback for target date checkbox
        :param event: generated event: Event
        :return: None
        """

        self.__update_date_view()

    def __on_button_get_rate(self, event: wx.Event):
        """
        Callback for get rate button
        :param event: generated event: Event
        :return: None
        """

        self.view.get_rate()

        if self.view.rate:
            self.rate_value.SetLabel(label=str(self.view.rate))
        else:
            self.rate_value.SetLabel(label='')
