"""
Log things for logging purposes.
"""
import logging
import sys
from typing import Union

LOG_FORMAT = '%(asctime)s [%(levelname)s] (%(name)s:%(lineno)d) - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class Logger:
    """
    Logger.
    """

    def __init__(self, logger_name: str, log_level: Union[int, str] = logging.INFO) -> None:
        """
        :param logger_name: logger name
        :param log_level: log level
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.logger.addHandler(self._create_console_handler())
        self.logger.propagate = False

    @staticmethod
    def _create_console_handler() -> logging.StreamHandler:
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
        console_handler.setFormatter(formatter)
        return console_handler
