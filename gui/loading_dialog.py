import wx
import wx.adv
import functools
import logging

from pubsub import pub
from data.loader import run_in_background
from utility.config import APP_NAME

logging.basicConfig(level=logging.INFO)


def load_process(method):

    @run_in_background
    def loading(func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            wx.CallAfter(pub.sendMessage, 'destroy')

            return result

        except Exception as err:
            logging.error(err)
            wx.CallAfter(pub.sendMessage, 'error', message=str(err))

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        thread = loading(method, *args, **kwargs)
        LoadingDialog(None, APP_NAME).ShowModal()

        return thread.join()

    return wrapper


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
