import json
import sys

from taskw import TaskWarrior
from taskw.fields import ArrayField
from taskw.task import Task

from twpm.hooks import example_hook


def on_add_runner():
    run('on_add')


def on_modify_runner():
    run('on_modify')


def to_output(task: dict) -> str:
    """
    Convert serialized task representation to hook output JSON
    """
    fields = Task.FIELDS.copy()

    for k, v in task.items():
        if isinstance(fields[k], ArrayField):
            task[k] = ','.join(v)

    return json.dumps(task, separators=(',', ':'))


def run(event):
    # Load task and Taskwarrior instance
    tw = TaskWarrior()
    udas = tw.config.get_udas()
    hook_task = Task(json.loads(sys.stdin.readline()), udas)

    # Run all active hooks
    example_hook.main(hook_task)

    # Export the final task after all active hooks have run
    # print(json.dumps(hook_task))
    print(json.dumps(hook_task.serialized(), separators=(',', ':')))

    # Exit
    sys.exit(0)
