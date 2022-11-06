"""
Hook to map tag shortcuts.
"""
import logging

from taskw.task import Task

logger = logging.getLogger(__name__)

TAG_MAP = {
    "n": "next",
    "@w": "@work",
    "@h": "@home",
}


def main(task: Task) -> None:
    """
    Inbox tag hook entry point.

    :param task: Task instance
    :return: None
    """
    task_tags = task.get('tags', [])

    new_tags = []
    for tag in task_tags:
        new_tag = TAG_MAP.get(tag, tag)
        new_tags.append(new_tag)
    if new_tags:
        task['tags'] = new_tags
