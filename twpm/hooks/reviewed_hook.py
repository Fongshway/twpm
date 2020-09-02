"""
Hook to set reviewed date UDA when modifying tasks.
"""
import logging
from datetime import datetime
from datetime import time

from dateutil import tz

from taskw.task import Task

logger = logging.getLogger(__name__)

DEFAULT_TIME = time(23, 59, 59)  # Your wanted default time


def set_default_time(timestamp: datetime) -> datetime:
    """
    Helper function to set the default timestamp for a given datetime.

    :param timestamp:
    :return: datetime with hour, minute, and second values to set the defaults.
    """
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
    reviewed_date = task.get('reviewed', None)
    print(reviewed_date)