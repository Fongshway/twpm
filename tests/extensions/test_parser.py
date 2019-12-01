"""
Tests for Taskwarrior data parser.
"""
from twpm.extensions.parser import parse_timewarrior_data
import datetime


def test_parse_timewarrior_data():
    now = datetime.datetime.now()
    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: off\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        f'[{{"start":"{one_hour_before_utc:%Y%m%dT%H%M%S}Z","end":"{now_utc:%Y%m%dT%H%M%S}Z","tags":["foo"]}}]',
    ]
    config, intervals = parse_timewarrior_data(input_stream)
    assert config == {
        'color': False,
        'debug': True,
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
