"""
Tests for Taskwarrior data parser.
"""
from twpm.extensions.parser import parse_timewarrior_data


def test_parse_empty_database(empty_database):
    input_stream, start, end = empty_database
    config, intervals = parse_timewarrior_data(input_stream)
    assert config == {
        'color': False,
        'debug': True,
        'temp.report.start': start,
        'temp.report.end': end,
    }
    assert intervals == []


def test_parse_filled_database(filled_database):
    input_stream, start, end = filled_database
    config, intervals = parse_timewarrior_data(input_stream)
    assert config == {
        'color': False,
        'debug': True,
        'temp.report.start': f'{start:%Y%m%dT%H%M%S}Z',
        'temp.report.end': f'{end:%Y%m%dT%H%M%S}Z',
    }
    assert intervals == [{
        "start": f"{start:%Y%m%dT%H%M%S}Z",
        "end": f"{end:%Y%m%dT%H%M%S}Z",
        "tags": ["foo"],
    }]
