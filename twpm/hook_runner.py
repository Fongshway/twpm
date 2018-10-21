"""
Hook runner
"""

import json
import sys

from taskw import TaskWarrior
from taskw.fields import ArrayField
from taskw.task import Task

from twpm.hooks import example_hook


def on_add_runner():
    """
    task on-add hook entry point.
    """
    run('on_add')


def on_modify_runner():
    """
    task on-modify hook entry point.
    """
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
    # pylint: disable=unused-argument
    """
    Main twpm hook runner entry point.
    """
    # Load task and Taskwarrior instance
    tw = TaskWarrior()
    udas = tw.config.get_udas()
    hook_task = Task(json.loads(sys.stdin.readline()), udas)

    # Run all active hooks
    example_hook.main(hook_task)

    # Export the final task after all active hooks have run
    print(to_output(hook_task.serialized()))

    # Exit
    sys.exit(0)
