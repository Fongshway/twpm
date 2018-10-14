#!/usr/bin/env python

import sys
import re
import json

added_task = json.loads(sys.stdin.readline())
original = added_task['description']
added_task['description'] = re.sub(r'\b(tw-\d+)\b',
                                   r'https://github.com/GothenburgBitFactory/taskwarrior/issues/\1',
                                   original,
                                   flags=re.IGNORECASE)
print(json.dumps(added_task))

if original != added_task['description']:
    print('Link added')

sys.exit(0)
