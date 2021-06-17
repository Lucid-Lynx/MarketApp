import wx
import wx.adv
import logging

from datetime import date
from web.client import Client
from utility.config import AVAILABLE_CURRENCIES

logging.basicConfig(level=logging.INFO)


class Gui:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Gui, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.app = wx.App()
        self.wnd = Window(None, 'MarketApp')

    def run(self):
        self.app.MainLoop()


class Window(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 500))
        self.data = Data()

        self.panel = wx.Panel(self)

        self.label_base_cur = wx.StaticText(self.panel, label='Base currency', pos=(10, 15))
        self.choice_base_cur = wx.Choice(self.panel, choices=[AVAILABLE_CURRENCIES[0]], pos=(130, 10))
        self.choice_base_cur.Bind(wx.EVT_CHOICE, self.on_choice)
        self.choice_base_cur.SetSelection(0)

        self.label_target_cur = wx.StaticText(self.panel, label='Target currency', pos=(10, 55))
        self.choice_target_cur = wx.Choice(self.panel, choices=AVAILABLE_CURRENCIES[1:], pos=(130, 50))
        self.choice_target_cur.Bind(wx.EVT_CHOICE, self.on_choice)
        self.choice_target_cur.SetSelection(0)

        self.label_mode = wx.StaticText(self.panel, label='Mode', pos=(10, 95))
        self.choice_mode = wx.Choice(self.panel, choices=['File', 'Remote'], pos=(130, 90))
        self.choice_mode.Bind(wx.EVT_CHOICE, self.on_choice)
        self.choice_mode.SetSelection(0)

        self.label_date = wx.StaticText(self.panel, label='Date', pos=(10, 135))
        self.calendar_date = wx.adv.CalendarCtrl(self.panel, pos=(130, 130))
        self.calendar_date.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, self.on_choice)

        self.button_rate = wx.Button(self.panel, label='Get rate', pos=(10, 175))
        self.button_rate.Bind(wx.EVT_BUTTON, self.on_button)

        self.label_rate = wx.StaticText(self.panel, label='Rate', pos=(10, 315))
        self.rate_value = wx.StaticText(self.panel, pos=(130, 315))

        self.Center()
        self.Show(True)

    def on_choice(self, event):
        self.data.base_cur = self.choice_base_cur.GetString(self.choice_base_cur.GetSelection())
        self.data.target_cur = self.choice_target_cur.GetString(self.choice_target_cur.GetSelection())
        self.data.mode = self.choice_mode.GetString(self.choice_mode.GetSelection())
        self.data.target_date = self.calendar_date.GetDate().Format(format='%d.%m.%Y')

    def on_button(self, event):
        self.on_choice(event)
        self.data.get_rate()
        self.rate_value.SetLabel(label=str(self.data.rate))


class Data:

    def __init__(
            self, base_cur=AVAILABLE_CURRENCIES[0], target_cur=AVAILABLE_CURRENCIES[0], mode='File',
            target_date=date.today()):
        self.base_cur = base_cur
        self.target_cur = target_cur
        self.mode = mode
        self.target_date = target_date
        self.rate = 0

    def get_rate(self):
        if self.mode == 'File':
            resp = Client(currencies=self.target_cur).get_curr_from_file()
        else:
            resp = Client(currencies=self.target_cur, date=self.target_date).get_curr_base()

        logging.info(resp)
        self.rate = resp['currencies'][self.target_cur]['base_value']
