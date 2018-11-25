# pylint: disable=missing-docstring
"""
Default time hook tests
"""
import uuid
from datetime import datetime, timedelta

from dateutil.tz import tzutc
from taskw.task import Task

from twpm.hooks import default_time_hook

NOW = datetime.now().replace(tzinfo=tzutc())


def test_default_time_hook():
    test_task = Task(
        {
            "status": "pending",
            "description": "Super urgent test task",
            "tags": ["@work"],
            "modified": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "entry": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "due": (NOW.replace(hour=0, minute=0, second=0) + timedelta(days=2)).strftime("%Y%m%dT%H%M%SZ"),
            "uuid": str(uuid.uuid4())
        }
    )
    default_time_hook.main(test_task)
    assert test_task['due'] == datetime(2018, 11, 26, 23, 59, 59, tzinfo=tzutc())
