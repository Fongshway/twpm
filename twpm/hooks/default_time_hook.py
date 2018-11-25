"""
Hook to set default timestamps when setting dates
"""
import logging
from datetime import time

from taskw.task import Task

logger = logging.getLogger(__name__)

DEFAULT_TIME = time(23, 59, 59)  # Your wanted default time


def set_default_time(timestamp):
    return timestamp.replace(
        hour=DEFAULT_TIME.hour,
        minute=DEFAULT_TIME.minute,
        second=DEFAULT_TIME.second,
    )


def main(task: Task) -> None:
    """
    Default time hook entry point.

    :param task: Task instance
    :return: None
    """
    due_date = task['due']
    if due_date and due_date.time() == time(0, 0, 0):
        task['due'] = set_default_time(task['due'])
        logger.info("Default due time has been set to %s", due_date)
