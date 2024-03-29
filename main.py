#!/usr/bin/python3
import logging

from decimal import setcontext, Context, ROUND_HALF_EVEN
# from web.client import Client
from gui.gui import Gui
from utility.config import PREC

logging.basicConfig(level=logging.INFO)


def app():
    """
    Main application loop. Runs GUI
    :return: None
    """

    context = Context(prec=PREC, rounding=ROUND_HALF_EVEN)
    setcontext(context)
    Gui().run()


'''
def app():
    """
    Main application loop. Runs menu
    :return: None
    """

    print('Choose currencies or skip:')
    currencies = input()
    print('Choose mode: file or remote:')
    mode = input()

    currencies = currencies.strip()
    mode = mode.strip()

    if mode not in ['file', 'remote']:
        err = 'Invalid mode'
        logging.error(err)
        raise ValueError(err)

    if mode == 'file':
        resp = Client(currencies=currencies).get_curr_from_file()
    else:
        print('Input date in format DD.MM.YYYY or skip:')
        date = input()
        resp = Client(currencies=currencies, date=date).get_curr_base()

    print(resp)
'''


def main():
    """
    Application entry point
    :return: None
    """

    try:
        app()

    except Exception as err:
        logging.error(err)


if __name__ == '__main__':
    main()
