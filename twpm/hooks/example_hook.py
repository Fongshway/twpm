"""
Example hook adapted from https://taskwarrior.org/docs/hooks_guide.html.
"""
import logging
import re

from taskw.task import Task

logger = logging.getLogger(__name__)


def main(task: Task) -> None:
    """
    example hook entry point.

    :param task: Task instance
    :return: None
    """
    original = task['description']
    task['description'] = re.sub(
        r'\b(tw-\d+)\b',
        r'https://github.com/GothenburgBitFactory/taskwarrior/issues/\1',
        original,
        flags=re.IGNORECASE
    )

    if original != task['description']:
        logger.info("Link added")
