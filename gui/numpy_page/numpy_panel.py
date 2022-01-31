import wx
import wx.adv
import platform

from utility.config import DATE_FORMAT
from gui.panel import Panel, handle_exception
from gui.numpy_page import PAGE_NAME
from gui.numpy_page.numpy_view import NumpyView
from stats.numpy_stats.numpy_stats import StatsNumpy


class NumpyPanel(Panel):
    """
    Panel for Numpy page
    """

    def __init__(self, parent: wx.Window, name: str = PAGE_NAME):
        super().__init__(parent, name=name)

        self.view = NumpyView()

        self.label_from_date = wx.StaticText(self, label='From', pos=(10, 95))
        self.calendar_from_date = wx.adv.CalendarCtrl(self, pos=(140, 90))
        self.calendar_from_date.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.__on_choice_from_date)

        self.label_to_date = wx.StaticText(self, label='To', pos=(390, 95))
        self.calendar_to_date = wx.adv.CalendarCtrl(self, pos=(520, 90))
        self.calendar_to_date.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.__on_choice_to_date)

        self.button_save_rate = wx.Button(self, label='Get stats', pos=(10, 135))
        self.button_save_rate.Bind(wx.EVT_BUTTON, self._on_button_get_stats)

        self.label_win_size = wx.StaticText(self, label='Window size', pos=(10, 275))
        self.win_size_value = wx.SpinCtrl(self, pos=(140, 270), min=1, initial=1)
        self.win_size_value.Bind(wx.EVT_SPINCTRL, self.__on_choice_win_size)

        self.label_sma = wx.StaticText(self, label='SMA', pos=(10, 315))
        self.sma_value = wx.StaticText(self, pos=(140, 310))

        self.label_average = wx.StaticText(self, label='Average', pos=(10, 355))
        self.average_value = wx.StaticText(self, pos=(140, 350))

        self.label_min = wx.StaticText(self, label='Min', pos=(10, 395))
        self.min_value = wx.StaticText(self, pos=(140, 390))

        self.label_max = wx.StaticText(self, label='Max', pos=(10, 435))
        self.max_value = wx.StaticText(self, pos=(140, 430))

        self._update_data()

    @handle_exception
    def _get_stats(self):
        """
        Compute all statistic metrics
        :return: None
        """

        self.view.save_rates()
        self.view.check_window_size()
        self.view.sma = StatsNumpy().sma(n=self.view.win_size)
        self.view.average = StatsNumpy().average()
        self.view.min = StatsNumpy().min()
        self.view.max = StatsNumpy().max()

    def _update_view(self):
        """
        Update view by data from panel
        :return: None
        """

        super()._update_view()
        self.__update_from_date_view()
        self.__update_to_date_view()

    @handle_exception
    def __update_from_date_view(self):
        """
        Update view for start date
        :return: None
        """

        new_date = self.calendar_from_date.GetDate().Format(format=DATE_FORMAT)

        if new_date != self.view.from_date:
            self.view.from_date = new_date

        to_date_obj = wx.DateTime()
        to_date_obj.ParseFormat(self.view.to_date, DATE_FORMAT)

        if platform.system() == 'Linux':
            self.calendar_from_date.SetDateRange(upperdate=to_date_obj)

    @handle_exception
    def __update_to_date_view(self):
        """
        Update view for finish date
        :return: None
        """

        new_date = self.calendar_to_date.GetDate().Format(format=DATE_FORMAT)

        if new_date != self.view.to_date:
            self.view.to_date = new_date

        from_date_obj = wx.DateTime()
        from_date_obj.ParseFormat(self.view.from_date, DATE_FORMAT)

        if platform.system() == 'Linux':
            self.calendar_to_date.SetDateRange(lowerdate=from_date_obj, upperdate=wx.DateTime.Today())

    def __on_choice_from_date(self, event: wx.Event):
        """
        Callback for start date calendar
        :param event: generated event: Event
        :return: None
        """

        self.__update_from_date_view()

    def __on_choice_to_date(self, event: wx.Event):
        """
        Callback for finish date calendar
        :param event: generated event: Event
        :return: None
        """

        self.__update_to_date_view()

    def _on_button_get_stats(self, event: wx.Event):
        """
        Callback for get stats button
        :param event: generated event: Event
        :return: None
        """

        self._get_stats()

        if self.view.sma:
            self.sma_value.SetLabel(label='   '.join(str(x) for x in self.view.sma))

        if self.view.average:
            self.average_value.SetLabel(label=str(self.view.average))
        else:
            self.average_value.SetLabel(label='')

        if self.view.min:
            self.min_value.SetLabel(label=str(self.view.min))
        else:
            self.min_value.SetLabel(label='')

        if self.view.max:
            self.max_value.SetLabel(label=str(self.view.max))
        else:
            self.max_value.SetLabel(label='')

    def __on_choice_win_size(self, event: wx.Event):
        """
        Callback for window size switcher
        :param event: generated event: Event
        :return: None
        """

        self.view.win_size = int(self.win_size_value.GetValue())
