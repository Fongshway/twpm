from twpm import hook_runner


def test_to_output():
    serialized_task = {
        'status': 'pending',
        'description': 'Fix tw-98765',
        'tags': ['in'],
        'modified': '20181018T050328Z',
        'entry': '20181018T050328Z',
        'uuid': 'd1b29100-3ee1-462e-b59e-4b570398b2d6'
    }
    expected = '{"status":"pending","description":"Fix tw-98765","tags":"in","modified":"20181018T050328Z","entry":"20181018T050328Z","uuid":"d1b29100-3ee1-462e-b59e-4b570398b2d6"}'

    result = hook_runner.to_output(serialized_task)

    assert result == expected
