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
    runner = HookRunner('on_add')
    runner.run()


def on_modify_runner():
    """
    task on-modify hook entry point.
    """
    runner = HookRunner('on_modify')
    runner.run()


class HookRunner:
    """
    Hook runner
    """

    def __init__(self, event, tw=TaskWarrior()):
        """
        Create an instance of HookRunner

        :param event: Hook event type
        :param tw: Taskwarrior instance
        """
        self.event = event
        self.tw = tw

    def from_input(self) -> Task:
        """
        Load task from input
        :return: hook_task
        """
        udas = self.tw.config.get_udas()
        if self.event == 'on_modify':
            task = Task.from_input(modify=True, udas=udas)
            return task
        task = Task.from_input(modify=False, udas=udas)
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
        # pylint: disable=unused-argument
        """
        Main twpm hook runner entry point.
        """
        # Load task from hook input
        input_task = self.from_input()

        # Run all active hooks
        example_hook.main(input_task)

        # Export the final task after all active hooks have run
        print(self.to_output(input_task))

        # Exit
        sys.exit(0)
