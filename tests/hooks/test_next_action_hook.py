"""
Next action hook tests.
"""
# pylint: disable=missing-docstring
import uuid
from copy import copy
from datetime import datetime
from logging.config import dictConfig

import pytest
from dateutil.tz import tzutc
from taskw.task import Task
from taskw.utils import DATE_FORMAT
from taskw.warrior import TaskWarrior

from twpm.hooks import next_action_hook

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] (%(name)s:%(lineno)d) - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "NOTSET",
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "twpm": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

NOW = datetime.now().replace(tzinfo=tzutc())


@pytest.fixture
def taskwarrior(tmp_path):
    taskrc_path = tmp_path.joinpath(".taskrc")
    taskrc_path.touch()

    config_overrides = {"data.location": str(tmp_path)}
    taskwarrior = TaskWarrior(config_filename=str(taskrc_path), config_overrides=config_overrides)
    assert taskwarrior.load_tasks() == {"completed": [], "pending": []}
    return taskwarrior


def test_next_action_hook_with_next(taskwarrior, capsys):
    dictConfig(LOGGING_CONFIG)

    # Setup - seed taskwarrior data with tasks
    taskwarrior.task_add("foobar", project="TEST")
    tasks = taskwarrior.load_tasks()
    assert len(tasks["pending"]) == 1

    test_task = Task(
        {
            "description": "test task 2",
            "project": "TEST",
            "tags": ["next"],
            "entry": NOW.strftime(DATE_FORMAT),
            "modified": NOW.strftime(DATE_FORMAT),
            "status": "pending",
            "uuid": str(uuid.uuid4()),
        }
    )
    next_action_hook.main(test_task, taskwarrior)
    assert "Project has a next action!" in capsys.readouterr().err


def test_complete_next_action(taskwarrior, capsys):
    """
    Confirm hook fires properly when the next action in a project is completed.
    """
    dictConfig(LOGGING_CONFIG)

    # Setup - seed taskwarrior data with tasks
    taskwarrior.task_add("foobar", project="TEST")
    test_task = taskwarrior.task_add("fizzbar", project="TEST", tags=["next"])
    tasks = taskwarrior.load_tasks()
    assert len(tasks["pending"]) == 2

    completed_task = copy(test_task)
    completed_task["status"] = "completed"
    next_action_hook.main(completed_task, taskwarrior)
    assert "Project does not have a next action!" in capsys.readouterr().err


def test_next_action_hook_with_many_next(taskwarrior, capsys):
    dictConfig(LOGGING_CONFIG)

    # Setup - seed taskwarrior data with tasks
    taskwarrior.task_add("foobar", project="TEST", tags=["next"])
    tasks = taskwarrior.load_tasks()
    assert len(tasks["pending"]) == 1

    test_task = Task(
        {
            "description": "test task 2",
            "project": "TEST",
            "tags": ["next"],
            "entry": NOW.strftime(DATE_FORMAT),
            "modified": NOW.strftime(DATE_FORMAT),
            "status": "pending",
            "uuid": str(uuid.uuid4()),
        }
    )
    next_action_hook.main(test_task, taskwarrior)
    assert "Project has more than one next action!" in capsys.readouterr().err


def test_next_action_hook_no_next(taskwarrior, capsys):
    dictConfig(LOGGING_CONFIG)

    # Setup - seed taskwarrior data with tasks
    taskwarrior.task_add("foobar", project="TEST")
    tasks = taskwarrior.load_tasks()
    assert len(tasks["pending"]) == 1

    test_task = Task(
        {
            "description": "test task 2",
            "project": "TEST",
            "entry": NOW.strftime(DATE_FORMAT),
            "modified": NOW.strftime(DATE_FORMAT),
            "status": "pending",
            "uuid": str(uuid.uuid4()),
        }
    )
    next_action_hook.main(test_task, taskwarrior)
    assert "Project does not have a next action!" in capsys.readouterr().err
