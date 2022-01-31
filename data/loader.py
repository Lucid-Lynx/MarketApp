import functools
import logging

from threading import Thread

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

        thread = Loader(method, *args, **kwargs)
        thread.start()

        return thread

    return wrapper


class Loader(Thread):
    """
    Loader thread for background process
    """

    def __init__(self, method, *args, **kwargs):
        super().__init__()
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.__return = None

    def run(self):
        """
        Run loader
        :return: None
        """

        logging.info('Start background process')
        self.__return = self.method(*self.args, **self.kwargs)

    def join(self, *args, **kwargs):
        """
        Join to the running thread and get return data
        :param args: list
        :param kwargs: dict
        :return: object
        """

        super().join(*args, **kwargs)

        return self.__return
