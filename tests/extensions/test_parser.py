"""
Tests for Taskwarrior data parser.
"""
from twpm.extensions.parser import parse_timewarrior_data


def test_parse_timewarrior_data(filled_database):
    input_stream, start, end = filled_database
    config, intervals = parse_timewarrior_data(input_stream)
    assert config == {
        'color': 'off',
        'debug': 'on',
        'temp.report.start': f'{start:%Y%m%dT%H%M%S}Z',
        'temp.report.end': f'{end:%Y%m%dT%H%M%S}Z',
    }
    assert intervals == [
        {
            "start": f"{start:%Y%m%dT%H%M%S}Z",
            "end": f"{end:%Y%m%dT%H%M%S}Z",
            "tags": ["foo"]
        }
    ]
