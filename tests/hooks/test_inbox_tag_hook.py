from taskw.task import Task

from twpm.hooks import inbox_tag_hook


def test_inbox_tag_hook_add():
    test_task = Task(
        {
            "description": "test task 1",
            "status": "pending",
            "tags": ["tag1", "tag2"],
            "modified": "20181015T054805Z",
            "entry": "20181015T054805Z",
            "uuid": "cee8cefa-0b9d-432c-a7da-cd68f50466bf"
        }
    )

    inbox_tag_hook.main(test_task)

    assert test_task['description'] == "test task 1"
    assert test_task['tags'] == ["tag1", "tag2", "in"]


def test_inbox_tag_hook_remove():
    test_task = Task(
        {
            "description": "test task 2",
            "status": "pending",
            "tags": ["@context", "tag1", "in"],
            "modified": "20181015T054805Z",
            "entry": "20181015T054805Z",
            "uuid": "cee8cefa-0b9d-432c-a7da-cd68f50466bf"
        }
    )

    inbox_tag_hook.main(test_task)

    assert test_task['description'] == "test task 2"
    assert test_task['tags'] == ["@context", "tag1"]
