# pylint: disable=missing-docstring
"""
Default time hook tests
"""
import uuid
from datetime import datetime, timedelta

from dateutil.tz import tzutc
from taskw.task import Task

from twpm.hooks import default_time_hook
from twpm.hooks.default_time_hook import DEFAULT_TIME

NOW = datetime.now().replace(tzinfo=tzutc())


def test_default_time_hook():
    due_date = NOW.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=2)
    wait_date = NOW.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    test_task = Task(
        {
            "status": "pending",
            "description": "Super urgent test task",
            "tags": ["@work"],
            "modified": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "entry": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "due": due_date.strftime("%Y%m%dT%H%M%SZ"),
            "wait": wait_date.strftime("%Y%m%dT%H%M%SZ"),
            "uuid": str(uuid.uuid4())
        }
    )
    default_time_hook.main(test_task)
    expected_due_date = due_date.replace(hour=DEFAULT_TIME.hour, minute=DEFAULT_TIME.minute, second=DEFAULT_TIME.second)
    expected_wait_date = wait_date.replace(hour=DEFAULT_TIME.hour, minute=DEFAULT_TIME.minute, second=DEFAULT_TIME.second)
    assert test_task['due'] == expected_due_date
    assert test_task['wait'] == expected_wait_date
