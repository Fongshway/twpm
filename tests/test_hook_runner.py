# pylint: disable=missing-docstring
"""
Hook runner tests
"""
from copy import deepcopy

from twpm.hook_runner import HookRunner


def test_to_output(tw):
    serialized_task = {
        'status': 'pending',
        'description': 'Fix tw-98765',
        'tags': ['in', 'next'],
        'modified': '20181018T050328Z',
        'entry': '20181018T050328Z',
        'uuid': 'd1b29100-3ee1-462e-b59e-4b570398b2d6'
    }
    expected = '{"status":"pending","description":"Fix tw-98765","tags":"in,next","modified":"20181018T050328Z",' \
               '"entry":"20181018T050328Z","uuid":"d1b29100-3ee1-462e-b59e-4b570398b2d6"}'

    on_add_runner = HookRunner('on_add', tw)
    on_modify_runner = HookRunner('on_modify', tw)

    on_add_result = on_add_runner.to_output(deepcopy(serialized_task))
    on_modify_result = on_modify_runner.to_output(deepcopy(serialized_task))

    assert on_add_result == expected
    assert on_modify_result == expected
