"""
Parser for Taskwarrior data.
"""
import json
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
                fields = line.strip().split(": ", 2)
                if len(fields) == 2:
                    config[fields[0]] = fields[1]
                else:
                    config[fields[0]] = ""
        # Extract interval entries
        else:
            body += line

    intervals = json.loads(body)
    return config, intervals
