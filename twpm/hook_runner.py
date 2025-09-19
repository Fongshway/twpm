"""
Hook runner.
"""
import json
import logging
import sys
import typing

import six
from taskw_ng import TaskWarrior
from taskw_ng.fields import AnnotationArrayField
from taskw_ng.fields import ArrayField
from taskw_ng.task import Task
from taskw_ng.utils import DATE_FORMAT

from twpm.hooks import default_time_hook
from twpm.hooks import inbox_tag_hook
from twpm.hooks import next_action_hook
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

    def __init__(self, event: str, tw: TaskWarrior | None = None) -> None:
        """
        Create an instance of HookRunner.

        :param event: Hook event type
        :param tw: Taskwarrior instance
        """
        self.event = event
        if tw is None:
            tw = TaskWarrior()
        self.tw = tw

    def from_input(self, hook_input: typing.IO[str] | six.StringIO = sys.stdin) -> Task:
        """
        Load task from input.

        :param hook_input: Taskwarrior JSON
        :return: Deserialized task
        """
        udas = self.tw.config.get_udas()
        if self.event == 'on_modify':
            task = Task.from_input(hook_input, modify=True, udas=udas)
            return typing.cast(Task, task)
        task = Task.from_input(hook_input, modify=False, udas=udas)
        return typing.cast(Task, task)

    @staticmethod
    def to_output(task: Task) -> str:
        """
        Convert Task() to Taskwarrior JSON string hook output format.

        :param task: Task instance
        :return: Taskwarrior JSON string
        """
        serialized_task: dict[str, typing.Any] = {}
        for k, v in task.items():
            field_type = task._fields.get(k, None)
            if isinstance(field_type, ArrayField) and not isinstance(field_type, AnnotationArrayField):
                serialized_task[k] = ','.join(task._serialize(k, v, task._fields))  # pylint: disable=protected-access
            elif isinstance(field_type, AnnotationArrayField):
                annotations = [
                    {
                        "entry": annotation.entry.strftime(DATE_FORMAT),
                        "description": annotation
                    } for annotation in v
                ]
                serialized_task[k] = annotations
            else:
                serialized_task[k] = task._serialize(k, v, task._fields)  # pylint: disable=protected-access
        return json.dumps(serialized_task, separators=(',', ':'), ensure_ascii=False)

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
        next_action_hook.main(input_task, self.tw)
        if self.event == 'on_modify':
            reviewed_hook.main(input_task)

        # Write the final task to stdout after all active hooks have run
        print(self.to_output(input_task))

        # Exit
        sys.exit(0)
