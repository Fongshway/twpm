#!/usr/bin/env python
###############################################################################
#
# Copyright 2015 - 2016, Paul Beckingham, Federico Hernandez.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://www.opensource.org/licenses/mit-license.php
#
###############################################################################
# pylint: disable=missing-function-docstring,missing-module-docstring
# pylint: disable=redefined-outer-name,too-many-branches,too-many-locals
# pylint: disable=too-many-statements
import datetime
import json
import sys
from typing import IO
from typing import Dict
from typing import List

from dateutil import tz

from twpm.extensions.parser import parse_timewarrior_data

DATEFORMAT = "%Y%m%dT%H%M%SZ"


def format_seconds(seconds: int) -> str:
    """Convert seconds to a formatted string

    Convert seconds: 3661
    To formatted: "   1:01:01"
    """
    hours = int(seconds / 3600)
    minutes = int(seconds % 3600 / 60)
    seconds = seconds % 60
    return f"{hours:4d}:{minutes:02d}:{seconds:02d}"


def calculate_totals(config: dict, intervals: list) -> List[str]:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # Sum the seconds tracked by tag.
    totals: Dict[str, datetime.timedelta] = dict()
    untagged = None
    for interval in intervals:
        start = datetime.datetime.strptime(interval["start"], DATEFORMAT)

        if "end" in interval:
            end = datetime.datetime.strptime(interval["end"], DATEFORMAT)
        else:
            end = datetime.datetime.utcnow()

        tracked = end - start

        if "tags" not in interval or interval["tags"] == []:
            if untagged is None:
                untagged = tracked
            else:
                untagged += tracked
        else:
            for tag in interval["tags"]:
                if tag in totals:
                    totals[tag] += tracked
                else:
                    totals[tag] = tracked

    # Determine largest tag width.
    max_width = len("Total")
    for tag in totals:
        if len(tag) > max_width:
            max_width = len(tag)

    if "temp.report.start" not in config:
        return ["There is no data in the database"]

    start_utc = datetime.datetime.strptime(config["temp.report.start"], DATEFORMAT)
    start_utc = start_utc.replace(tzinfo=from_zone)
    start = start_utc.astimezone(to_zone)

    if "temp.report.end" in config:
        end_utc = datetime.datetime.strptime(config["temp.report.end"], DATEFORMAT)
        end_utc = end_utc.replace(tzinfo=from_zone)
        end = end_utc.astimezone(to_zone)
    else:
        end = datetime.datetime.now()

    if len(totals) == 0 and untagged is None:
        return ["No data in the range {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}".format(start, end)]

    # Compose report header.
    output = [
        "",
        "Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}".format(start, end),
        "",
    ]

    # Compose table header.
    if config["color"] == "on":
        output.append("[4m{:{width}}[0m [4m{:>10}[0m".format("Tag", "Total", width=max_width))
    else:
        output.append("{:{width}} {:>10}".format("Tag", "Total", width=max_width))
        output.append("{} {}".format("-" * max_width, "----------"))

    # Compose table rows.
    grand_total = 0
    for tag in sorted(totals):
        seconds = int(totals[tag].total_seconds())
        formatted = format_seconds(seconds)
        grand_total += seconds
        output.append("{:{width}} {:10}".format(tag, formatted, width=max_width))

    if untagged is not None:
        seconds = int(untagged.total_seconds())
        formatted = format_seconds(seconds)
        grand_total += seconds
        output.append("{:{width}} {:10}".format("", formatted, width=max_width))

    # Compose total.
    if config["color"] == "on":
        output.append("{} {}".format(" " * max_width, "[4m          [0m"))
    else:
        output.append("{} {}".format(" " * max_width, "----------"))

    output.append("{:{width}} {:10}".format("Total", format_seconds(grand_total), width=max_width))
    output.append("")

    return output


if __name__ == "__main__":
    config, intervals = parse_timewarrior_data(sys.stdin)
    for line in calculate_totals(config, intervals):
        print(line)
