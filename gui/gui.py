import wx
import wx.adv

from utility.config import APP_NAME
from gui.window import Window


class Gui:
    """
    Gui entrypoint class
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Gui, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.app = wx.App(False)
        self.wnd = Window(None, APP_NAME)
        self.app.Bind(wx.EVT_WINDOW_DESTROY, self.__on_exit)

    def run(self):
        """
        Run GUI main loop
        :return: None
        """

        self.app.MainLoop()

    def stop(self):
        """
        Stop GUI main loop
        :return: None
        """

        self.app.ExitMainLoop()

    def __on_exit(self, event):
        """
        Callback for closing window event
        :param event: Event
        :return: None
        """

        self.stop()
