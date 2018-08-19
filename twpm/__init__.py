from hook_utils import find_hooks
from tasklib import Task
from taskw import TaskWarrior
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def hook_runner(event):
    task = Task.from_input()
    warrior = TaskWarrior

    for hook in find_hooks(event):
        logging.debug(' Running %s', hook.__name__)
        hook(task)

    print task.export_data()
