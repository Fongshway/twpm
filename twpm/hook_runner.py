import json
import sys

from twpm.hooks import example_hook


def on_add_runner():
    run('on_add')


def on_modify_runner():
    run('on_modify')


def run(event):
    # Load task and Taskwarrior instance
    hook_task = json.loads(sys.stdin.readline())

    # Run all active hooks
    example_hook.main(hook_task)

    # Export the final task after all active hooks have run
    print(json.dumps(hook_task))

    # Exit
    sys.exit(0)
