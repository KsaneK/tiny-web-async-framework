import logging
import sys
from functools import partial

import termcolor as termcolor


def log(param):
    def wrapper(cls, logger_class=ColoredLogger):
        cls.logger = logger_class(cls.__name__)
        return cls

    if issubclass(param, ColoredLogger):
        return partial(wrapper, logger_class=param)

    param.logger = ColoredLogger(param.__name__)
    return param


class ColoredLogger:
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    def __init__(
        self,
        name,
        level=logging.INFO,
        log_file=None,
        log_to_console=True,
        log_to_file=False,
    ):
        self.log_file = log_file
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if log_to_console:
            self.create_console_handler()
        if log_to_file:
            self.create_file_handler()

    def create_console_handler(self):
        handler = logging.StreamHandler(sys.stdout)
        self.set_formatter(handler)
        self.logger.addHandler(handler)

    def create_file_handler(self):
        handler = logging.FileHandler(self.log_file)
        self.set_formatter(handler)
        self.logger.addHandler(handler)

    @staticmethod
    def set_formatter(handler):
        formatter = logging.Formatter(ColoredLogger.LOG_FORMAT)
        handler.setFormatter(formatter)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(termcolor.colored(message, color="cyan"), *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.logger.info(termcolor.colored(message, color="green"), *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(termcolor.colored(message, color="yellow"), *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(termcolor.colored(message, color="red"), *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(termcolor.colored(message, on_color="red"), *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self.logger.exception(message, *args, **kwargs)


class RequestLogger(ColoredLogger):
    def log(self, message, status_code, *args, **kwargs):
        if 100 <= status_code < 400:
            log_func = self.info
        elif 400 <= status_code < 500:
            log_func = self.warning
        else:
            log_func = self.error

        log_func(message, *args, **kwargs)
