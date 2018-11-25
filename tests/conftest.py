# pylint: disable=redefined-outer-name
"""
Pytest fixtures.
"""
import os
import shutil
import tempfile

import pytest
from taskw import TaskWarrior


@pytest.fixture
def default_taskrc_path():
    """
    Path to default taskrc resource.
    """
    path_to_default_taskrc = os.path.join(os.path.dirname(__file__), 'resources/default.taskrc')
    yield path_to_default_taskrc


@pytest.fixture
def tw(default_taskrc_path):
    """
    TaskWarrior instance that uses default.taskrc.
    """
    taskdata = tempfile.mkdtemp()
    tw = TaskWarrior(config_filename=default_taskrc_path, config_overrides={'data.location': taskdata})
    yield tw
    shutil.rmtree(taskdata)
