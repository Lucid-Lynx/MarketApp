import functools
import logging

logging.basicConfig(level=logging.INFO)


def run_in_background(method):

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        return Loader(method, *args, **kwargs).run()

    return wrapper


class Loader:

    def __init__(self, method, *args, **kwargs):
        super().__init__()
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def run(self):
        logging.info('Start background process')
        return self.method(*self.args, **self.kwargs)
