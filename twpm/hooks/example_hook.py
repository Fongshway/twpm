#!/usr/bin/env python

import re

from taskw.task import Task


def main(task: Task):
    print()
    original = task['description']
    task['description'] = re.sub(
        r'\b(tw-\d+)\b',
        r'https://github.com/GothenburgBitFactory/taskwarrior/issues/\1',
        original,
        flags=re.IGNORECASE
    )

    if original != task['description']:
        print('Link added')
