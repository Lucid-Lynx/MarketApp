import wx
import wx.adv
import functools
import platform
import logging

from pubsub import pub
from data.loader import run_in_background
from utility.config import APP_NAME

logging.basicConfig(level=logging.INFO)


def load_process(method):
    """
    Decorator for download processes, which shows loading dialog
    :param method: decorated method
    :return: wrapper for decorated method
    """

    @run_in_background
    def loading(func, *args, **kwargs):
        """
        Run decorated method with dialog message
        :param func: decorated method
        :param args: list
        :param kwargs: dict
        :return: object
        """
        try:
            result = func(*args, **kwargs)
            wx.CallAfter(pub.sendMessage, 'destroy')

            return result

        except Exception as err:
            logging.error(err)
            wx.CallAfter(pub.sendMessage, 'error', message=str(err))

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        """
        Run thread with decorated method and show modal window
        :param args: list
        :param kwargs: dict
        :return: return data from thread: object
        """

        thread = loading(method, *args, **kwargs)

        if platform.system() == 'Linux':
            LoadingDialog(None, APP_NAME).ShowModal()

        return thread.join()

    return wrapper


class LoadingDialog(wx.Dialog):
    """
    Class for loading dialog
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LoadingDialog, cls).__new__(cls)

        return cls.instance

    def __init__(self, parent: wx.Window, title: str):
        super().__init__(parent, title=title, size=(200, 100))

        self.panel = wx.Panel(self)
        self.label_loading = wx.StaticText(self.panel, label='Loading...', pos=(10, 15))

        pub.subscribe(self.__on_destroy, 'destroy')
        pub.subscribe(self.__on_error, 'error')
        self.Center()

    def __on_destroy(self):
        """
        Destroy loading dialog
        :return: None
        """

        self.Destroy()

    def __on_error(self, message: str):
        """
        Show error dialog
        :param message: error message: str
        :return: None
        """

        self.__on_destroy()
        wx.MessageDialog(self, message=message, style=wx.OK | wx.ICON_ERROR).ShowModal()
