"""
Hook to set default timestamps when setting dates
"""
import logging
from datetime import time

from taskw.task import Task

logger = logging.getLogger(__name__)

DEFAULT_TIME = time(23, 59, 59)  # Your wanted default time


def main(task: Task) -> None:
    """
    Default time hook entry point.

    :param task: Task instance
    :return: None
    """
    logging.info(' Default due time has been set.')
