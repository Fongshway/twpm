from twpm.hooks import example_hook


def run(event):
    # Load task and taskwarrior instance

    # Run all active hooks
    example_hook.main()

    # Export the final task after all active hooks have run
