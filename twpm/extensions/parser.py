"""
Parser for Taskwarrior data.
"""
import json
import re
from io import StringIO
from typing import Tuple


def parse_timewarrior_data(input_stream: StringIO) -> Tuple[dict, list]:
    """
    Parse data passed to report from timewarrior.
    """
    header = 1
    config = dict()
    body = ""
    for line in input_stream.readlines():
        # Extract the configuration settings.
        if header:
            if line == "\n":
                header = 0
            else:
                match = re.search('^([^:]+): (.*)$', line, re.MULTILINE)
                if match:
                    config[match.group(1)] = match.group(2)
        # Extract interval entries
        else:
            body += line
    remap = {
        'on': True,
        'off': False,
        '': None,
    }
    clean_config = {k: remap.get(v, v) for k, v in config.items()}

    intervals = json.loads(body)
    return clean_config, intervals
