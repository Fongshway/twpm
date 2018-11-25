"""
Hook to help flag tasks without a context
"""
import logging

from taskw.task import Task

logger = logging.getLogger(__name__)


def main(task: Task) -> None:
    """
    Inbox tag hook entry point.

    :param task: Task instance
    :return: None
    """
    # Handle case when task has no context tags and no inbox tag.
    if not any('@' in t for t in task['tags']) and u'in' not in task['tags']:
        logger.info("Task has no context tag - inbox tag will be applied")
        task['tags'].append('in')

    # Handle case when task has context tag and inbox tag.
    elif any('@' in t for t in task['tags']) and u'in' in task['tags']:
        logger.info("Task has both context and inbox tags - inbox tag will be removed.")
        task['tags'].remove('in')
