import wx
import wx.adv
import logging

from utility.config import APP_NAME
from .widgets import Window

logging.basicConfig(level=logging.INFO)


class Gui:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Gui, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.app = wx.App()
        self.wnd = Window(None, APP_NAME)

    def run(self):
        self.update_window()
        self.app.MainLoop()

    def update_window(self):
        self.wnd.update_data()
