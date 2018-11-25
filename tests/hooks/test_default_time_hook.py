# pylint: disable=missing-docstring
"""
Default time hook tests
"""
import uuid
from datetime import datetime, timedelta

import dateutil
import pytz
from dateutil.tz import tzutc
from taskw.task import Task
from taskw.utils import DATE_FORMAT

from twpm.hooks import default_time_hook
from twpm.hooks.default_time_hook import DEFAULT_TIME

LOCAL_TZ = dateutil.tz.tzlocal()
NOW = datetime.now()


def test_default_time_midnight():
    due_date = NOW.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=LOCAL_TZ) + timedelta(days=2)
    wait_date = NOW.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=LOCAL_TZ) + timedelta(days=1)

    test_task = Task(
        {
            "status": "pending",
            "description": "Super urgent test task",
            "tags": ["@work"],
            "modified": NOW.strftime(DATE_FORMAT),
            "entry": NOW.strftime(DATE_FORMAT),
            "due": due_date.astimezone(pytz.utc).strftime(DATE_FORMAT),
            "wait": wait_date.astimezone(pytz.utc).strftime(DATE_FORMAT),
            "uuid": str(uuid.uuid4())
        }
    )
    default_time_hook.main(test_task)
    expected_due = due_date.replace(hour=DEFAULT_TIME.hour, minute=DEFAULT_TIME.minute, second=DEFAULT_TIME.second, tzinfo=tzutc())
    expected_wait = wait_date.replace(hour=DEFAULT_TIME.hour, minute=DEFAULT_TIME.minute, second=DEFAULT_TIME.second, tzinfo=tzutc())
    assert test_task['due'] == expected_due
    assert test_task['wait'] == expected_wait


def test_default_time_not_midnight():
    due_date = NOW.replace(second=1, microsecond=0) + timedelta(days=2)
    wait_date = NOW.replace(second=1, microsecond=0) + timedelta(days=1)

    test_task = Task(
        {
            "status": "pending",
            "description": "Super urgent test task",
            "tags": ["@work"],
            "modified": NOW.strftime(DATE_FORMAT),
            "entry": NOW.strftime(DATE_FORMAT),
            "due": due_date.strftime(DATE_FORMAT),
            "wait": wait_date.strftime(DATE_FORMAT),
            "uuid": str(uuid.uuid4())
        }
    )
    default_time_hook.main(test_task)
    assert test_task['due'] == due_date.replace(tzinfo=tzutc())
    assert test_task['wait'] == wait_date.replace(tzinfo=tzutc())
