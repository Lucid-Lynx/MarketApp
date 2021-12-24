import wx
import wx.adv
import logging

from utility.config import APP_NAME
from gui.window import Window

logging.basicConfig(level=logging.INFO)


class Gui:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Gui, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.app = wx.App(False)
        self.wnd = Window(None, APP_NAME)

        self.app.Bind(wx.EVT_WINDOW_DESTROY, self.__on_exit)

    def run(self):
        self.app.MainLoop()

    def stop(self):
        self.app.ExitMainLoop()

    def __on_exit(self, event):
        self.stop()
