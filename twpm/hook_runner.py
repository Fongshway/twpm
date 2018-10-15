from twpm.hooks.test_hook import main


def run(event):
    # Load task and taskwarrior instance

    # Run all active hooks
    main()

    # Export the final task after all active hooks have run
