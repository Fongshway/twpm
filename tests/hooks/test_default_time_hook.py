# pylint: disable=missing-docstring
"""
Default time hook tests
"""
import uuid
from datetime import datetime

import pytz
from taskw.task import Task

from twpm.hooks import default_time_hook


NOW = datetime.now().replace(tzinfo=pytz.UTC)


def test_default_time_hook():
    test_task = Task(
        {
            "status": "pending",
            "description": "Super urgent test task",
            "tags": ["@work"],
            "modified": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "entry": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "due": datetime(2018, 11, 25, 0, 0, 0).replace(tzinfo=pytz.UTC).strftime("%Y%m%dT%H%M%SZ"),
            "uuid": str(uuid.uuid4())
        }
    )

    default_time_hook.main(test_task)

    assert test_task['description'] == "Fix https://github.com/GothenburgBitFactory/taskwarrior/issues/tw-98765"
