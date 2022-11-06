"""
Hook determine if project has a next action.
"""
import logging
from collections import Counter

from taskw.task import Task
from taskw.warrior import TaskWarrior

logger = logging.getLogger(__name__)


def main(task: Task, tw: TaskWarrior) -> None:
    """
    Inbox tag hook entry point.

    :param task: Task instance
    :return: None
    """
    task_project = task.get("project")

    if not task_project:
        return

    task_filter = {
        "status": "pending",
        "project": task_project,
    }
    project_tasks = tw.filter_tasks(task_filter)

    tag_counter = Counter()
    for project_task in project_tasks:
        project_task_tags = project_task.get("tags")
        if project_task_tags:
            for tag in project_task_tags:
                tag_counter[tag] += 1

    task_tags = task.get("tags")
    if task_tags:
        for tag in task_tags:
            tag_counter[tag] += 1
    next_tag_count = tag_counter["next"]
    if next_tag_count == 1:
        logger.debug("Project has a next action!")
    elif next_tag_count > 1:
        logger.warning("Project has more than one next action!")
    else:
        logger.warning("Project does not have a next action!")
