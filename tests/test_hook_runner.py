# pylint: disable=missing-docstring
"""
Hook runner tests
"""
import os
import shutil
import tempfile
from copy import deepcopy

import pytest
from taskw import TaskWarrior

from twpm.hook_runner import HookRunner


@pytest.fixture
def default_taskrc_path():
    """ Path to default taskrc resource """
    path_to_default_taskrc = os.path.join(os.path.dirname(__file__), 'resources/default.taskrc')
    yield path_to_default_taskrc


@pytest.fixture
def tw(default_taskrc_path):
    """ TaskWarrior instance that uses default.taskrc"""
    taskdata = tempfile.mkdtemp()
    tw = TaskWarrior(config_filename=default_taskrc_path, config_overrides={'data.location': taskdata})
    yield tw
    shutil.rmtree(taskdata)


def test_to_output(tw):
    serialized_task = {
        'status': 'pending',
        'description': 'Fix tw-98765',
        'tags': ['in', 'next'],
        'modified': '20181018T050328Z',
        'entry': '20181018T050328Z',
        'uuid': 'd1b29100-3ee1-462e-b59e-4b570398b2d6'
    }
    expected = '{"status":"pending","description":"Fix tw-98765","tags":"in,next","modified":"20181018T050328Z",' \
               '"entry":"20181018T050328Z","uuid":"d1b29100-3ee1-462e-b59e-4b570398b2d6"}'

    on_add_runner = HookRunner('on_add', tw)
    on_modify_runner = HookRunner('on_modify', tw)

    on_add_result = on_add_runner.to_output(deepcopy(serialized_task))
    on_modify_result = on_modify_runner.to_output(deepcopy(serialized_task))

    assert on_add_result == expected
    assert on_modify_result == expected
