"""
Tag map shortcuts hook tests.
"""
# pylint: disable=missing-docstring
import uuid
from datetime import datetime

from dateutil.tz import tzutc
from taskw.task import Task
from taskw.utils import DATE_FORMAT

from twpm.hooks import tag_map_hook

NOW = datetime.now().replace(tzinfo=tzutc())


def test_tag_map():
    test_task = Task(
        {
            "description": "test task 1",
            "status": "pending",
            "tags": ["tag1", "n", "@w", "@h", "ne"],
            "modified": NOW.strftime(DATE_FORMAT),
            "entry": NOW.strftime(DATE_FORMAT),
            "uuid": str(uuid.uuid4()),
        }
    )

    tag_map_hook.main(test_task)

    assert test_task['description'] == "test task 1"
    assert test_task['tags'] == ["tag1", "next", "@work", "@home", "ne"]


def test_tag_map_no_tags():
    test_task = Task(
        {
            "description": "test task 2",
            "entry": NOW.strftime(DATE_FORMAT),
            "modified": NOW.strftime(DATE_FORMAT),
            "status": "pending",
            "uuid": str(uuid.uuid4()),
        }
    )

    tag_map_hook.main(test_task)

    assert test_task['description'] == "test task 2"
    assert test_task.get('tags') is None
