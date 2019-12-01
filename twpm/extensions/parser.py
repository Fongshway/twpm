"""
Parser for Taskwarrior data.
"""
import json
import re
from io import StringIO


def parse_timewarrior_data(input_stream: StringIO) -> (dict, list):
    header = 1
    config = dict()
    body = ""
    for line in input_stream.readlines():
        # Extract the configuration settings.
        if header:
            if line == "\n":
                header = 0
            else:
                m = re.search('^([^:]+): (.*)$', line, re.MULTILINE)
                config[m.group(1)] = m.group(2)
        # Extract interval entries
        else:
            body += line

    intervals = json.loads(body)
    return config, intervals
