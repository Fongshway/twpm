"""
Test for setting reviewed UDA on modified tasks.
"""
import uuid
from datetime import datetime

import pytz
from dateutil.tz import tzutc
from taskw.fields import DateField
from taskw.task import Task
from taskw.utils import DATE_FORMAT
from datetime import timedelta
from twpm.hooks import reviewed_hook
from twpm.hooks.reviewed_hook import DEFAULT_TIME

NOW = datetime.now()


def test_reviewed():
    entry_date = NOW - timedelta(days=1)
    task_data = {
            "status": "pending",
            "description": "Super urgent test task",
            "tags": ["@home"],
            "entry": entry_date.strftime(DATE_FORMAT),
            "uuid": str(uuid.uuid4())
        }
    task_udas = {
        "reviewed": DateField(label="Reviewed"),
    }
    test_task = Task(task_data, task_udas)
    reviewed_hook.main(test_task)
    assert test_task['reviewed'] == NOW.replace(
        hour=DEFAULT_TIME.hour,
        minute=DEFAULT_TIME.minute,
        second=DEFAULT_TIME.second,
        tzinfo=tzutc(),
    )
