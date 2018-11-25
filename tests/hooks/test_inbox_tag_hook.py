# pylint: disable=missing-docstring
"""
Inbox tag hook tests
"""
import uuid
from datetime import datetime

from dateutil.tz import tzutc
from taskw.task import Task

from twpm.hooks import inbox_tag_hook

NOW = datetime.now().replace(tzinfo=tzutc())


def test_inbox_tag_add():
    test_task = Task(
        {
            "description": "test task 1",
            "status": "pending",
            "tags": ["tag1", "tag2"],
            "modified": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "entry": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "uuid": str(uuid.uuid4())
        }
    )

    inbox_tag_hook.main(test_task)

    assert test_task['description'] == "test task 1"
    assert test_task['tags'] == ["tag1", "tag2", "in"]


def test_inbox_tag_remove():
    test_task = Task(
        {
            "description": "test task 2",
            "status": "pending",
            "tags": ["@context", "tag1", "in"],
            "modified": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "entry": NOW.strftime("%Y%m%dT%H%M%SZ"),
            "uuid": str(uuid.uuid4())
        }
    )

    inbox_tag_hook.main(test_task)

    assert test_task['description'] == "test task 2"
    assert test_task['tags'] == ["@context", "tag1"]
