"""
Hook runner
"""

import json
import logging
import sys
from typing import IO

from taskw import TaskWarrior
from taskw.fields import ArrayField
from taskw.task import Task

from twpm.hooks import example_hook
from twpm.hooks import default_time_hook
from twpm.hooks import inbox_tag_hook

logger = logging.getLogger(__name__)


def on_add_runner() -> None:
    """
    task on-add hook entry point.
    """
    runner = HookRunner('on_add')
    runner.run()


def on_modify_runner() -> None:
    """
    task on-modify hook entry point.
    """
    runner = HookRunner('on_modify')
    runner.run()


class HookRunner:
    """
    Hook runner
    """

    def __init__(self, event: str, tw: TaskWarrior = TaskWarrior()) -> None:
        """
        Create an instance of HookRunner

        :param event: Hook event type
        :param tw: Taskwarrior instance
        """
        self.event = event
        self.tw = tw

    def from_input(self, hook_input: IO[str] = sys.stdin) -> Task:
        """
        Load task from input
        :return: hook_task
        """
        udas = self.tw.config.get_udas()
        if self.event == 'on_modify':
            task = Task.from_input(hook_input, modify=True, udas=udas)
            return task
        task = Task.from_input(hook_input, modify=False, udas=udas)
        return task

    @staticmethod
    def to_output(task: dict) -> str:
        """
        Convert serialized task representation to hook output JSON
        """
        fields = Task.FIELDS.copy()

        for k, v in task.items():
            if isinstance(fields[k], ArrayField):
                task[k] = ','.join(v)

        return json.dumps(task, separators=(',', ':'))

    def run(self) -> None:
        # pylint: disable=fixme
        """
        Main twpm hook runner entry point.
        """
        # Load task from hook input
        input_task = self.from_input()

        # Run all active hooks
        # TODO Expose ability to define hooks in .taskrc (e.g. twpm.hooks = inbox_tag_hook,default_time_hook)
        example_hook.main(input_task)
        inbox_tag_hook.main(input_task)
        default_time_hook.main(input_task)

        # Write the final task to stdout after all active hooks have run
        print(self.to_output(input_task.serialized()))

        # Exit
        sys.exit(0)
