from taskw.task import Task

from twpm import hook_runner


def test_to_output():
    input = {'status': 'pending', 'description': 'Fix tw-98765',
     'tags': ['in'], 'modified': '20181018T050328Z', 'entry': '20181018T050328Z',
     'uuid': 'd1b29100-3ee1-462e-b59e-4b570398b2d6'}
    expected = '{"status":"pending","description":"Fix tw-98765","tags":"in","modified":"20181018T050328Z","entry":"20181018T050328Z","uuid":"d1b29100-3ee1-462e-b59e-4b570398b2d6"}'

    result = hook_runner.to_output(input)

    assert result == expected

