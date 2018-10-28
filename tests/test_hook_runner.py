# pylint: disable=missing-docstring
"""
Hook runner tests
"""
import datetime
import uuid
from copy import deepcopy

import six
from dateutil.tz import tzutc

from twpm.hook_runner import HookRunner


def test_from_input(tw):
    input_add_data = six.StringIO(
        '{'
        '"description":"Go to Camelot",'
        '"entry":"20180618T030242Z",'
        '"status":"pending",'
        '"start":"20181012T110605Z",'
        '"uuid":"daa3ff05-f716-482e-bc35-3e1601e50778"'
        '}'
    )
    input_modify_data = six.StringIO(
        '\n'.join(
            [
                input_add_data.getvalue(),
                (
                    '{'
                    '"description":"Go to Camelot again",'
                    '"entry":"20180618T030242Z",'
                    '"status":"pending",'
                    '"start":"20181012T110605Z",'
                    '"uuid":"daa3ff05-f716-482e-bc35-3e1601e50778"'
                    '}'
                ),
            ]
        ),
    )
    on_add_runner = HookRunner('on_add', tw)
    on_add_task_actual = on_add_runner.from_input(input_add_data)
    assert on_add_task_actual['description'] == "Go to Camelot"
    assert on_add_task_actual['entry'] == datetime.datetime(2018, 6, 18, 3, 2, 42, tzinfo=tzutc())
    assert on_add_task_actual['status'] == "pending"
    assert on_add_task_actual['start'] == datetime.datetime(2018, 10, 12, 11, 6, 5, tzinfo=tzutc())
    assert on_add_task_actual['uuid'] == uuid.UUID("daa3ff05-f716-482e-bc35-3e1601e50778")

    on_modify_runner = HookRunner('on_modify', tw)
    on_modify_task_actual = on_modify_runner.from_input(input_modify_data)
    assert on_modify_task_actual['description'] == "Go to Camelot again"


def test_to_output(tw):
    serialized_task = {
        'status': 'pending',
        'description': 'Fix tw-98765',
        'tags': ['in', 'next'],
        'modified': '20181018T050328Z',
        'entry': '20181018T050328Z',
        'uuid': 'd1b29100-3ee1-462e-b59e-4b570398b2d6'
    }
    expected_output = '{"status":"pending","description":"Fix tw-98765","tags":"in,next",' \
                      '"modified":"20181018T050328Z","entry":"20181018T050328Z",' \
                      '"uuid":"d1b29100-3ee1-462e-b59e-4b570398b2d6"}'

    on_add_runner = HookRunner('on_add', tw)
    on_modify_runner = HookRunner('on_modify', tw)

    on_add_result = on_add_runner.to_output(deepcopy(serialized_task))
    on_modify_result = on_modify_runner.to_output(deepcopy(serialized_task))

    assert on_add_result == expected_output
    assert on_modify_result == expected_output
