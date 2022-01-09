#!/usr/bin/python3
import os
import logging

from datetime import datetime
from decimal import setcontext, Context, ROUND_HALF_EVEN
from parser_tools.parser import Parser
from utility.config import PREC, DATE_FORMAT

logging.basicConfig(level=logging.INFO)


class Data:

    def __new__(cls, *args, **kwargs):
        pass

    def __init__(self, currencies=None, date=None):
        pass

    def get_curr_from_file(self):
        pass


def app():
    pass


def main():
    pass


if __name__ == '__main__':
    main()
