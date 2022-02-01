import functools
import logging

logging.basicConfig(level=logging.INFO)


def run_in_background(method):
    """
    Decorator for background processes
    :param method: Decorated method
    :return: Wrapper for decorated process
    """

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        """
        Wrapper for decorated process
        :param args: list
        :param kwargs: dict
        :return: background thread: Thread
        """

        return Loader(method, *args, **kwargs).run()

    return wrapper


class Loader:
    """
    Loader thread for background process
    """

    def __init__(self, method, *args, **kwargs):
        super().__init__()
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Run loader
        :return: None
        """

        logging.info('Start background process')
        return self.method(*self.args, **self.kwargs)
