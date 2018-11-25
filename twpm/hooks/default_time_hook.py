"""
Hook to set default timestamps when setting dates
"""
import logging

from taskw.task import Task

logger = logging.getLogger(__name__)


def main(task: Task) -> None:
    """
    Default time hook entry point.

    :param task: Task instance
    :return: None
    """
    logging.info(' Default due time has been set.')
