"""
Hook runner.
"""
import logging
import sys
from typing import IO
from typing import Union

import six
from taskw import TaskWarrior
from taskw.task import Task

from twpm.hooks import default_time_hook
from twpm.hooks import inbox_tag_hook
from twpm.hooks import reviewed_hook
from twpm.hooks import tag_map_hook

logger = logging.getLogger(__name__)


def on_add_runner() -> None:
    """
    task on-add hook entry point.
    """
    runner = HookRunner('on_add')
    logger.debug("Running on-add hooks")
    runner.run()


def on_modify_runner() -> None:
    """
    task on-modify hook entry point.
    """
    runner = HookRunner('on_modify')
    logger.debug("Running on-modify hooks")
    runner.run()


class HookRunner:
    """
    Hook runner.
    """

    def __init__(self, event: str, tw: TaskWarrior = TaskWarrior()) -> None:
        """
        Create an instance of HookRunner.

        :param event: Hook event type
        :param tw: Taskwarrior instance
        """
        self.event = event
        self.tw = tw

    def from_input(self, hook_input: Union[IO[str], six.StringIO] = sys.stdin) -> Task:
        """
        Load task from input.

        :param hook_input: Taskwarrior JSON
        :return: Deserialized task
        """
        udas = self.tw.config.get_udas()
        if self.event == 'on_modify':
            task = Task.from_input(hook_input, modify=True, udas=udas)
            return task
        task = Task.from_input(hook_input, modify=False, udas=udas)
        return task

    @staticmethod
    def to_output(task: Task) -> str:
        """
        Convert Task() to Taskwarrior JSON string hook output format.

        :param task: Task instance
        :return: Taskwarrior JSON string
        """
        return str(task)

    def run(self) -> None:
        # pylint: disable=fixme
        """
        Main twpm hook runner entry point.
        """
        # Load task from hook input
        input_task = self.from_input()

        # Run all active hooks
        # TODO Expose ability to define hooks in .taskrc (e.g. twpm.hooks = inbox_tag_hook,default_time_hook)
        tag_map_hook.main(input_task)
        inbox_tag_hook.main(input_task)
        default_time_hook.main(input_task)
        if self.event == 'on_modify':
            reviewed_hook.main(input_task)

        # Write the final task to stdout after all active hooks have run
        print(self.to_output(input_task))

        # Exit
        sys.exit(0)
