"""
Hook to set default timestamps when setting dates.
"""
import logging
from datetime import datetime
from datetime import time

from dateutil import tz

from taskw.task import Task

logger = logging.getLogger(__name__)

DEFAULT_TIME = time(23, 59, 59)  # Your wanted default time


def is_local_midnight(timestamp: datetime) -> bool:
    """
    Helper function to evaluate whether or not a dateime is midnight in local
    time.

    :param timestamp:
    :return: Boolean indicating if the datetime is midnight in local time.
    """
    return timestamp.astimezone(tz.tzlocal()).time() == time(0, 0, 0)


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
        tzinfo=tz.tzlocal(),
    )


def main(task: Task) -> None:
    # pylint: disable=fixme
    """
    Default time hook entry point.

    :param task: Task instance
    :return: None
    """
    # TODO Expose ability to set dates to apply hook to in .taskrc (e.g. twpm.hook.dates = due,wait)
    task_due_date = task.get('due', None)

    # Exit hook if task has no due date
    if not task_due_date:
        return

    if task_due_date.time() and is_local_midnight(task_due_date):
        task['due'] = set_default_time(task['due'])
        logger.info("Default due time has been set to %s", task['due'].strftime("%Y-%m-%d %H:%M:%S %Z"))

    task_wait_date = task.get('wait', None)

    # Exit hook if task has no wait date
    if not task_wait_date:
        return

    if task_wait_date.time() and is_local_midnight(task_wait_date):
        task['wait'] = set_default_time(task['wait'])
        logger.info("Default wait time has been set to %s", task['wait'].strftime("%Y-%m-%d %H:%M:%S %Z"))
