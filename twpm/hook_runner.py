from twpm.hooks import example_hook


def on_add_runner():
    run('on_add')


def on_modify_runner():
    run('on_modify')


def run(event):
    # Load task and taskwarrior instance

    # Run all active hooks
    example_hook.main()

    # Export the final task after all active hooks have run
