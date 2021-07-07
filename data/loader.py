import functools
import logging

from threading import Thread

logging.basicConfig(level=logging.INFO)


def run_in_background(method):

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        thread = Loader(method, *args, **kwargs)
        thread.start()

    return wrapper


class Loader(Thread):

    def __init__(self, method, *args, **kwargs):
        super().__init__()
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def run(self):
        logging.info('Start background process')
        self.method(*self.args, **self.kwargs)
