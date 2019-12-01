"""
Tests for Taskwarrior data parser.
"""
from twpm.extensions.parser import parse_timewarrior_data
import datetime
from io import StringIO


def test_parse_timewarrior_data():
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
    config, intervals = parse_timewarrior_data(StringIO(input_stream))
    assert config == {
        'color': 'off',
        'debug': 'on',
        'temp.report.start': f'{one_hour_before_utc:%Y%m%dT%H%M%S}Z',
        'temp.report.end': f'{now_utc:%Y%m%dT%H%M%S}Z',
    }
    assert intervals == [
        {
            "start": f"{one_hour_before_utc:%Y%m%dT%H%M%S}Z",
            "end": f"{now_utc:%Y%m%dT%H%M%S}Z",
            "tags": ["foo"]
        }
    ]
