"""
Timewarrior extension pytest fixtures.
"""
import datetime
from io import StringIO

import pytest


@pytest.fixture
def empty_database():
    input_stream = ''.join([
        'color: off\n',
        'debug: on\n',
        'temp.report.start: \n',
        'temp.report.end: \n',
        '\n',
        '[]',
    ])
    return StringIO(input_stream), None, None


@pytest.fixture
def filled_database():
    now = datetime.datetime.now()
    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = ''.join([
        'color: off\n',
        'debug: on\n',
        f'temp.report.start: {one_hour_before_utc:%Y%m%dT%H%M%S}Z\n',
        f'temp.report.end: {now_utc:%Y%m%dT%H%M%S}Z\n',
        '\n',
        f'[{{"start":"{one_hour_before_utc:%Y%m%dT%H%M%S}Z","end":"{now_utc:%Y%m%dT%H%M%S}Z","tags":["foo"]}}]',
    ])
    return StringIO(input_stream), one_hour_before_utc, now_utc
