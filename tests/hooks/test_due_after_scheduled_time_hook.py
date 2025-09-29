# pylint: disable=missing-docstring
from datetime import datetime

from dateutil import tz
from taskw_ng.task import Task

from twpm.hooks import due_after_scheduled_time_hook


def test_due_is_after_scheduled_time():
    test_task = Task(
        {
            "status": "pending",
            "description": "Scheduled date is after due date",
            "tags": ["@work"],
            "modified": "20250928T170312Z",
            "entry": "20250928T170312Z",
            "due": "20251003T070000Z",
            "scheduled": "20251004T000000Z",
            "wait": "20250929T070000Z",
            "uuid": "8fff2ff7-39d8-42b7-88c6-fc8c4cda0f17",
        }
    )

    due_after_scheduled_time_hook.main(test_task)
    assert test_task["due"] == datetime(
        year=2025,
        month=10,
        day=4,
        hour=23,
        minute=59,
        second=59,
        tzinfo=tz.tzlocal(),
    )


def test_due_is_not_after_scheduled_time():
    test_task = Task(
        {
            "status": "pending",
            "description": "Scheduled date is not after due date",
            "tags": ["@work"],
            "modified": "20250928T170312Z",
            "entry": "20250928T170312Z",
            "due": "20251004T000000Z",
            "scheduled": "20251001T000000Z",
            "wait": "20250929T070000Z",
            "uuid": "8fff2ff7-39d8-42b7-88c6-fc8c4cda0f17",
        }
    )

    due_after_scheduled_time_hook.main(test_task)
    assert test_task == Task(
        {
            "status": "pending",
            "description": "Scheduled date is not after due date",
            "tags": ["@work"],
            "modified": "20250928T170312Z",
            "entry": "20250928T170312Z",
            "due": "20251004T000000Z",
            "scheduled": "20251001T000000Z",
            "wait": "20250929T070000Z",
            "uuid": "8fff2ff7-39d8-42b7-88c6-fc8c4cda0f17",
        }
    )
