"""
Parser for Taskwarrior data.
"""
import json

from typing.io import IO


def parse_timewarrior_data(input_stream: str) -> dict:
    # Extract the configuration settings.
    header = 1
    config = dict()
    body = ""
    for line in input_stream.split('\n'):
        if header:
            if line == "":
                header = 0
            else:
                fields = line.strip().split(": ", 2)
                if len(fields) == 2:
                    config[fields[0]] = fields[1]
                else:
                    config[fields[0]] = ""
        else:
            body += line

    intervals = json.loads(body)
    return config, intervals
