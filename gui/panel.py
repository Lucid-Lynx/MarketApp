import wx.adv
import functools
import logging

from gui.view import View

logging.basicConfig(level=logging.INFO)


def handle_exception(method):
    """
    Decorator for showing error messages with dialog
    :param method: decorated method
    :return: wrapper for decorated method
    """

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        """
        Wrapper for decorated method
        :param args: list
        :param kwargs: dict
        :return: None
        """

        try:
            method(*args, **kwargs)
        except Exception as err:
            logging.error(err)
            wx.MessageDialog(args[0], message=str(err), style=wx.OK | wx.ICON_ERROR).ShowModal()

    return wrapper


class Panel(wx.Panel):
    """
    Base panel for each page
    """

    def __init__(self, parent: wx.Window, name: str):
        super().__init__(parent, name=name)
        self.view = View()

        self.label_base_cur = wx.StaticText(self, label='Base currency', pos=(10, 15))
        self.choice_base_cur = wx.Choice(self, choices=self.view.get_available_bases(), pos=(140, 10))
        self.choice_base_cur.Bind(wx.EVT_CHOICE, self._on_choice_currency)
        self.choice_base_cur.SetSelection(0)

        self.label_target_cur = wx.StaticText(self, label='Target currency', pos=(10, 55))
        self.choice_target_cur = wx.Choice(self, choices=self.view.get_available_targets(), pos=(140, 50))
        self.choice_target_cur.Bind(wx.EVT_CHOICE, self._on_choice_currency)
        self.choice_target_cur.SetSelection(0)

        self.button_clean = wx.Button(self, label='Clean store', pos=(10, 475))
        self.button_clean.Bind(wx.EVT_BUTTON, self.__on_button_clean)

    def _collect_data(self):
        """
        Get current data from cache and set in the view
        :return: None
        """

        self.view.get_data()
        self._update_view()

    def _update_data(self):
        """
        Update data in view
        :return: None
        """

        self._collect_data()

    def _update_view(self):
        """
        Update view by data from panel
        :return: None
        """

        self.__update_checkboxes()
        self.__update_currency_views()

    def __update_checkboxes(self):
        """
        Update checkboxes
        :return: None
        """

        self._update_base_cur_checkbox()
        self._update_target_cur_checkbox()
        self.choice_base_cur.SetSelection(0)
        self.choice_target_cur.SetSelection(0)

    def __update_currency_views(self):
        """
        Update base and target currency fields in view
        :return: None
        """

        new_base_cur = self.choice_base_cur.GetStringSelection()
        new_target_cur = self.choice_target_cur.GetStringSelection()

        if new_base_cur != self.view.base_cur:
            self.view.base_cur = new_base_cur
            self._update_target_cur_checkbox()

        if new_target_cur in self.view.get_available_targets():
            self.choice_target_cur.SetSelection(self.choice_target_cur.FindString(new_target_cur))
        else:
            self.choice_target_cur.SetSelection(0)
            new_target_cur = self.choice_target_cur.GetStringSelection()

        self.view.target_cur = new_target_cur

    def _update_base_cur_checkbox(self):
        """
        Update base currency checkbox
        :return: None
        """

        self.choice_base_cur.Clear()
        self.choice_base_cur.AppendItems(self.view.get_available_bases())

    def _update_target_cur_checkbox(self):
        """
        Update target currency checkbox
        :return: None
        """

        self.choice_target_cur.Clear()
        self.choice_target_cur.AppendItems(self.view.get_available_targets())

    def _on_choice_currency(self, event: wx.Event):
        """
        Callback for currency checkboxes
        :param event: generated event: Event
        :return: None
        """

        self.__update_currency_views()

    def __on_button_clean(self, event: wx.Event):
        """
        Callback for clean button
        :param event: generated event: Event
        :return: None
        """

        self.view.store.clean()
