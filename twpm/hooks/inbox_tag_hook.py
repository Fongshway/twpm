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
    task_tags = task.get('tags', [])

    # Exit hook if task has no tags
    if not task_tags:
        return

    # Handle case when task has no context tags and no inbox tag.
    if not any('@' in t for t in task_tags) and "in" not in task_tags:
        task['tags'].append('in')
        logger.info("Task had no context tag - inbox tag has be applied")

    # Handle case when task has context tag and inbox tag.
    elif any('@' in t for t in task_tags) and u'in' in task_tags:
        task['tags'].remove('in')
        logger.info("Task had both context and inbox tags - inbox tag has been removed.")
