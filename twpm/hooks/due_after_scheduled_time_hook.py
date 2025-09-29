"""
Hook to update due date if scheduled date is after the due date.
"""

import logging
from datetime import datetime
from datetime import time

from dateutil import tz
from taskw_ng.task import Task

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


def set_default_time(due_date: datetime, scheduled_date: datetime) -> datetime:
    """
    Helper function to set the default timestamp for a given datetime.

    :param timestamp:
    :return: datetime with hour, minute, and second values to set the defaults.
    """
    return due_date.replace(
        year=scheduled_date.year,
        month=scheduled_date.month,
        day=scheduled_date.day,
        hour=DEFAULT_TIME.hour,
        minute=DEFAULT_TIME.minute,
        second=DEFAULT_TIME.second,
        tzinfo=tz.tzlocal(),
    )


def main(task: Task) -> None:
    # pylint: disable=fixme
    """
    Hook entry point.

    :param task: Task instance
    :return: None
    """
    task_scheduled_date = task.get("scheduled", None)
    task_due_date = task.get("due", None)
    if task_due_date is None or task_scheduled_date is None:
        return

    if task_scheduled_date > task_due_date:
        task["due"] = set_default_time(task_due_date, task_scheduled_date)
        logger.info(
            "'Scheduled' date is after the 'due' date. The 'due' date has been set to %s",
            task["due"].strftime("%Y-%m-%d %H:%M:%S %Z"),
        )
