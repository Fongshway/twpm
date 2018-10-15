from twpm.hooks import test_hook


def run(event):
    # Load task and taskwarrior instance

    # Run all active hooks
    test_hook.main()

    # Export the final task after all active hooks have run
