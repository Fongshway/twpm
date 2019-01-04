# pylint: disable=missing-docstring
"""
Hook runner tests.
"""
import uuid
from copy import deepcopy
from datetime import datetime

import six
from dateutil.tz import tzutc
from taskw.task import Task
from taskw.utils import DATE_FORMAT

from twpm.hook_runner import HookRunner

NOW = datetime.now().replace(tzinfo=tzutc())


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
    assert on_add_task_actual['entry'] == datetime(2018, 6, 18, 3, 2, 42, tzinfo=tzutc())
    assert on_add_task_actual['status'] == "pending"
    assert on_add_task_actual['start'] == datetime(2018, 10, 12, 11, 6, 5, tzinfo=tzutc())
    assert on_add_task_actual['uuid'] == uuid.UUID("daa3ff05-f716-482e-bc35-3e1601e50778")

    on_modify_runner = HookRunner('on_modify', tw)
    on_modify_task_actual = on_modify_runner.from_input(input_modify_data)
    assert on_modify_task_actual['description'] == "Go to Camelot again"
    assert on_modify_task_actual['entry'] == datetime(2018, 6, 18, 3, 2, 42, tzinfo=tzutc())
    assert on_modify_task_actual['status'] == "pending"
    assert on_modify_task_actual['start'] == datetime(2018, 10, 12, 11, 6, 5, tzinfo=tzutc())
    assert on_modify_task_actual['uuid'] == uuid.UUID("daa3ff05-f716-482e-bc35-3e1601e50778")


def test_to_output(tw):
    test_uuid = str(uuid.uuid4())
    test_task = Task(
        {
            'annotations': [{
                'entry': '20190103T051020Z',
                'description': 'yoooooo'
            }],
            'status': 'pending',
            'description': 'Fix tw-98765',
            'tags': ['in', 'next'],
            'modified': NOW.strftime(DATE_FORMAT),
            'entry': NOW.strftime(DATE_FORMAT),
            'reviewed': NOW.strftime(DATE_FORMAT),
            'uuid': test_uuid
        }
    )
    expected_output = "".join(
        [
            '{',
            '"annotations":[{"entry":"20190103T051020Z","description":"yoooooo"}],',
            '"status":"pending",',
            '"description":"Fix tw-98765",',
            '"tags":"in,next",',
            '"modified":"{}",'.format(NOW.strftime(DATE_FORMAT)),
            '"entry":"{}",'.format(NOW.strftime(DATE_FORMAT)),
            '"reviewed":"{}",'.format(NOW.strftime(DATE_FORMAT)),
            '"uuid":"{}"'.format(test_uuid),
            '}',
        ]
    )

    on_add_result = HookRunner('on_add', tw).to_output(test_task.serialized())
    on_modify_result = HookRunner('on_modify', tw).to_output(test_task.serialized())

    assert on_add_result == expected_output
    assert on_modify_result == expected_output
