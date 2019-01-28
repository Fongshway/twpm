"""
Hook runner.
"""
import json
import logging
import sys
from typing import IO
from typing import Union

import click
import six
from taskw import TaskWarrior
from taskw.fields import AnnotationArrayField
from taskw.fields import ArrayField
from taskw.task import Task

from twpm.hooks import default_time_hook
from twpm.hooks import example_hook
from twpm.hooks import inbox_tag_hook

logger = logging.getLogger(__name__)


@click.command()
@click.argument('api', type=str)
@click.argument('args', type=str)
@click.argument('command', type=str)
@click.argument('rc', type=str)
@click.argument('data', type=str)
@click.argument('version', type=str)
def on_add_runner(api, args, command, rc, data, version) -> None:
    """
    task on-add hook entry point.
    """
    print(api)
    print(args)
    print(command)
    print(rc)
    print(data)
    print(version)

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


class HookMeta:

    def __init__(self, api, args, command, rc, data, version):
        self.api = self._parse_api(api)
        self.args = self._parse_args(args)
        self.command = self._parse_command(command)
        self.rc = self._parse_rc(rc)
        self.data = self._parse_data(data)
        self.version = self._parse_version(version)

    @staticmethod
    def _parse_api(api):
        return api

    @staticmethod
    def _parse_args(args):
        return args

    @staticmethod
    def _parse_command(command):
        return command

    @staticmethod
    def _parse_rc(rc):
        return rc

    @staticmethod
    def _parse_data(data):
        return data

    @staticmethod
    def _parse_version(version):
        return version


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
    def to_output(task: dict) -> str:
        """
        Convert serialized task representation to Taskwarrior JSON hook output
        format.

        :param task: serialized task
        :return: Taskwarrior JSON
        """
        fields = Task.FIELDS.copy()

        for k, v in task.items():
            field_type = fields.get(k, None)
            if isinstance(field_type, ArrayField) and not isinstance(field_type, AnnotationArrayField):
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
