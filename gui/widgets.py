import wx
import wx.adv
import logging

from pubsub import pub
from utility.config import APP_NAME
from data.loader import run_in_background
from .view import View

logging.basicConfig(level=logging.INFO)


class Window(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 500))

        self.view = View()
        self.panel = wx.Panel(self)

        self.label_base_cur = wx.StaticText(self.panel, label='Base currency', pos=(10, 15))
        self.choice_base_cur = wx.Choice(self.panel, choices=self.view.get_available_bases(), pos=(130, 10))
        self.choice_base_cur.Bind(wx.EVT_CHOICE, self.__on_choice)
        self.choice_base_cur.SetSelection(0)

        self.label_target_cur = wx.StaticText(self.panel, label='Target currency', pos=(10, 55))
        self.choice_target_cur = wx.Choice(self.panel, choices=self.view.get_available_targets(), pos=(130, 50))
        self.choice_target_cur.Bind(wx.EVT_CHOICE, self.__on_choice)
        self.choice_target_cur.SetSelection(0)

        self.label_mode = wx.StaticText(self.panel, label='Mode', pos=(10, 95))
        self.choice_mode = wx.Choice(self.panel, choices=['Remote', 'File'], pos=(130, 90))
        self.choice_mode.Bind(wx.EVT_CHOICE, self.__on_choice)
        self.choice_mode.SetSelection(0)

        self.label_date = wx.StaticText(self.panel, label='Date', pos=(10, 135))
        self.calendar_date = wx.adv.CalendarCtrl(self.panel, pos=(130, 130))
        self.calendar_date.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.__on_choice)

        self.button_rate = wx.Button(self.panel, label='Get rate', pos=(10, 175))
        self.button_rate.Bind(wx.EVT_BUTTON, self.__on_button_get_rate)

        self.button_update = wx.Button(self.panel, label='Update data', pos=(10, 215))
        self.button_update.Bind(wx.EVT_BUTTON, self.__on_button_update)

        self.label_rate = wx.StaticText(self.panel, label='Rate', pos=(10, 315))
        self.rate_value = wx.StaticText(self.panel, pos=(130, 315))

        self.__update_view()
        self.Center()
        self.Show(True)

    def update_data(self):
        self.__update_process()
        LoadingDialog(None, APP_NAME).ShowModal()

    @run_in_background
    def __update_process(self):
        try:
            self.view.update_data()
            self.__update_checkboxes()
            wx.CallAfter(pub.sendMessage, 'destroy')

        except Exception as err:
            logging.error(err)
            wx.CallAfter(pub.sendMessage, 'error', message=str(err))

    def __update_view(self):
        self.__change_currency()
        self.__change_date()
        self.view.mode = self.choice_mode.GetStringSelection()

    def __change_currency(self):
        new_base_cur = self.choice_base_cur.GetStringSelection()
        new_target_cur = self.choice_target_cur.GetStringSelection()

        if new_base_cur != self.view.base_cur:
            self.view.base_cur = new_base_cur
            self.__update_target_cur_checkbox()
            self.view.store.change_base_currency(base_currency=new_base_cur)

        if new_target_cur in self.view.get_available_targets():
            self.choice_target_cur.SetSelection(self.choice_target_cur.FindString(new_target_cur))
        else:
            self.choice_target_cur.SetSelection(0)
            new_target_cur = self.choice_target_cur.GetStringSelection()

        self.view.target_cur = new_target_cur

    def __change_date(self):
        new_date = self.calendar_date.GetDate().Format(format='%d.%m.%Y')

        if new_date != self.view.target_date:
            self.view.target_date = new_date
            self.update_data()

    def __update_base_cur_checkbox(self):
        self.choice_base_cur.Clear()
        self.choice_base_cur.AppendItems(self.view.get_available_bases())

    def __update_target_cur_checkbox(self):
        self.choice_target_cur.Clear()
        self.choice_target_cur.AppendItems(self.view.get_available_targets())

    def __update_checkboxes(self):
        self.__update_base_cur_checkbox()
        self.__update_target_cur_checkbox()
        self.choice_base_cur.SetSelection(0)
        self.choice_target_cur.SetSelection(0)

    def __on_choice(self, event):
        self.__update_view()

    def __on_button_get_rate(self, event):
        self.view.get_rate()

        if self.view.rate:
            self.rate_value.SetLabel(label=str(self.view.rate))
        else:
            self.rate_value.SetLabel(label='')

    def __on_button_update(self, event):
        self.update_data()


class LoadingDialog(wx.Dialog):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LoadingDialog, cls).__new__(cls)

        return cls.instance

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(200, 100))

        self.panel = wx.Panel(self)
        self.label_loading = wx.StaticText(self.panel, label='Loading...', pos=(10, 15))

        pub.subscribe(self.__on_destroy, 'destroy')
        pub.subscribe(self.__on_error, 'error')
        self.Center()

    def __on_destroy(self):
        self.Destroy()

    def __on_error(self, message):
        self.__on_destroy()
        wx.MessageDialog(self, message=message, style=wx.OK | wx.ICON_ERROR).ShowModal()
