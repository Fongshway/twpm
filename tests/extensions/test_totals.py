"""
Tests for totals Timewarrior extension report.
"""
import datetime

from twpm.extensions.totals import calculate_totals
from twpm.extensions.totals import format_seconds


def test_totals_with_empty_database():
    """
    totals extension should report error on empty database
    """
    input_stream = [
        'color: off\n',
        'debug: on\n',
        'temp.report.start: \n',
        'temp.report.end: \n',
        '\n',
        '[]',
    ]
    expected_output = ['There is no data in the database']
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_with_filled_database():
    """totals extension should print report for filled database"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

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
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now),
        '',
        'Tag        Total',
        '----- ----------',
        'foo      1:00:00',
        '      ----------',
        'Total    1:00:00',
        '',
    ]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_with_time_delta_larger_than_24_hours():
    """
    totals extension should print report for time delta larger than 24 hours
    """
    now = datetime.datetime.now()
    two_days_before = now - datetime.timedelta(days=2)

    now_utc = now.utcnow()
    two_days_before_utc = now_utc - datetime.timedelta(days=2)

    input_stream = [
        'color: off\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(two_days_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        f'[{{"start":"{two_days_before_utc:%Y%m%dT%H%M%S}Z","end":"{now_utc:%Y%m%dT%H%M%S}Z","tags":["foo"]}}]',
    ]
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(two_days_before, now),
        '',
        'Tag        Total',
        '----- ----------',
        'foo     48:00:00',
        '      ----------',
        'Total   48:00:00',
        '',
    ]

    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_with_emtpy_range():
    """totals extension should report error on emtpy range"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: off\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        '[]',
    ]
    out = calculate_totals(input_stream)
    assert ['No data in the range {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now)] == out


def test_totals_with_interval_without_tags():
    """totals extension should handle interval without tags"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: off\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        f'[{{"start":"{one_hour_before_utc:%Y%m%dT%H%M%S}Z","end":"{now_utc:%Y%m%dT%H%M%S}Z"}}]',
    ]
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now),
        '',
        'Tag        Total',
        '----- ----------',
        '         1:00:00',
        '      ----------',
        'Total    1:00:00',
        '',
    ]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_with_interval_with_empty_tag_list():
    """totals extension should handle interval with empty tag list"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: off\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        '[{{"start":"{:%Y%m%dT%H%M%S}Z","end":"{:%Y%m%dT%H%M%S}Z","tags":[]}}]'.format(one_hour_before_utc, now_utc),
    ]
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now),
        '',
        'Tag        Total',
        '----- ----------',
        '         1:00:00',
        '      ----------',
        'Total    1:00:00',
        '',
    ]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_with_open_interval(self):
    """totals extension should handle open interval"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: off\n',
        'debug: off\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: \n',
        '\n',
        '[{{"start":"{:%Y%m%dT%H%M%S}Z","tags":["foo"]}}]'.format(one_hour_before_utc),
    ]
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now),
        '',
        'Tag        Total',
        '----- ----------',
        'foo      1:00:00',
        '      ----------',
        'Total    1:00:00',
        '',
    ]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_colored_with_empty_database(self):
    """totals extension should report error on empty database (colored)"""
    input_stream = [
        'color: on\n',
        'debug: on\n',
        'temp.report.start: \n',
        'temp.report.end: \n',
        '\n',
        '[]',
    ]
    expected_output = ['There is no data in the database']
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_colored_with_filled_database(self):
    """totals extension should print report for filled database (colored)"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: on\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        f'[{{"start":"{one_hour_before_utc:%Y%m%dT%H%M%S}Z","end":"{now_utc:%Y%m%dT%H%M%S}Z","tags":["foo"]}}]',
    ]
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now),
        '',
        '[4mTag  [0m [4m     Total[0m',
        'foo      1:00:00',
        '      [4m          [0m',
        'Total    1:00:00',
        '',
    ]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_colored_with_emtpy_range(self):
    """totals extension should report error on emtpy range (colored)"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: on\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        '[]',
    ]
    expected_output = ['No data in the range {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now)]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_colored_with_interval_without_tags(self):
    """totals extension should handle interval without tags (colored)"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: on\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        '[{{"start":"{:%Y%m%dT%H%M%S}Z","end":"{:%Y%m%dT%H%M%S}Z"}}]'.format(one_hour_before_utc, now_utc),
    ]
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now),
        '',
        '[4mTag  [0m [4m     Total[0m',
        '         1:00:00',
        '      [4m          [0m',
        'Total    1:00:00',
        '',
    ]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_colored_with_interval_with_empty_tag_list(self):
    """totals extension should handle interval with empty tag list (colored)"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: on\n',
        'debug: on\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: {:%Y%m%dT%H%M%S}Z\n'.format(now_utc),
        '\n',
        '[{"start":"20160101T070000Z","end":"20160101T080000Z","tags":[]}]',
    ]
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now),
        '',
        '[4mTag  [0m [4m     Total[0m',
        '         1:00:00',
        '      [4m          [0m',
        'Total    1:00:00',
        '',
    ]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_totals_colored_with_open_interval(self):
    """totals extension should handle open interval (colored)"""
    now = datetime.datetime.now()
    one_hour_before = now - datetime.timedelta(hours=1)

    now_utc = now.utcnow()
    one_hour_before_utc = now_utc - datetime.timedelta(hours=1)

    input_stream = [
        'color: on\n',
        'debug: off\n',
        'temp.report.start: {:%Y%m%dT%H%M%S}Z\n'.format(one_hour_before_utc),
        'temp.report.end: \n',
        '\n',
        '[{{"start":"{:%Y%m%dT%H%M%S}Z","tags":["foo"]}}]'.format(one_hour_before_utc),
    ]
    expected_output = [
        '',
        'Total by Tag, for {:%Y-%m-%d %H:%M:%S} - {:%Y-%m-%d %H:%M:%S}'.format(one_hour_before, now),
        '',
        '[4mTag  [0m [4m     Total[0m',
        'foo      1:00:00',
        '      [4m          [0m',
        'Total    1:00:00',
        '',
    ]
    actual_output = calculate_totals(input_stream)
    assert actual_output == expected_output


def test_format_seconds_with_less_than_1_minute(self):
    """Test format_seconds with less than 1 minute"""
    self.assertEqual(format_seconds(34), '   0:00:34')


def test_format_seconds_with_1_minute(self):
    """Test format_seconds with 1 minute"""
    self.assertEqual(format_seconds(60), '   0:01:00')


def test_format_seconds_with_1_hour(self):
    """Test format_seconds with 1 hour"""
    self.assertEqual(format_seconds(3600), '   1:00:00')


def test_format_seconds_with_more_than_1_hour(self):
    """Test format_seconds with more than 1 hour"""
    self.assertEqual(format_seconds(3645), '   1:00:45')
