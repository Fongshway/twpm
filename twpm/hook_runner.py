import json
import sys

from taskw import TaskWarrior
from taskw.task import Task

from twpm.hooks import example_hook


def on_add_runner():
    run('on_add')


def on_modify_runner():
    run('on_modify')


def run(event):
    # Load task and Taskwarrior instance
    tw = TaskWarrior()
    udas = tw.config.get_udas()
    hook_task = Task(json.loads(sys.stdin.readline()), udas)

    # Run all active hooks
    example_hook.main(hook_task)

    # Export the final task after all active hooks have run
    print(json.dumps(hook_task))

    # Exit
    sys.exit(0)
