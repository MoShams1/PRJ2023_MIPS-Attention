from psychopy import event, core


def escape_session():
    exit_key = event.getKeys(keyList=['escape'])
    if 'escape' in exit_key:
        core.quit()
