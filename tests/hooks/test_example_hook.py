from taskw.task import Task

from twpm.hooks import example_hook


def test_example_hook():
    test_task = Task({"status": "pending", "description": "Fix tw-98765", "tags": "in", "modified": "20181015T054805Z",
                 "entry": "20181015T054805Z", "uuid": "cee8cefa-0b9d-432c-a7da-cd68f50466bf"})

    example_hook.main(test_task)

    assert test_task['description'] == "Fix https://github.com/GothenburgBitFactory/taskwarrior/issues/tw-98765"
