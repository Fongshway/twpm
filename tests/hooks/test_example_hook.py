# pylint: disable=missing-docstring
"""
Example hook tests.
"""
import uuid
from datetime import datetime

from dateutil.tz import tzutc

from taskw.task import Task
from twpm.hooks import example_hook

NOW = datetime.now().replace(tzinfo=tzutc())


def test_example():
    test_task = Task(
        {
            "status": "pending",
            "description": "Fix tw-98765",
            "tags": ["in"],
            "modified": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "entry": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "uuid": str(uuid.uuid4())
        }
    )

    example_hook.main(test_task)

    assert test_task['description'] == "Fix https://github.com/GothenburgBitFactory/taskwarrior/issues/tw-98765"
