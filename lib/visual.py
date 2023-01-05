import numpy as np
from psychopy import monitors, visual, event, core


def configmon_imac():
    monitor = monitors.Monitor('prim_mon', width=54.7, distance=57)
    monitor.setSizePix([2240, 1260])
    return monitor


def configmon_macair():
    monitor = monitors.Monitor('prim_mon', width=33.78, distance=57)
    monitor.setSizePix([1440, 900])
    return monitor


def configmon_dell():
    monitor = monitors.Monitor('prim_mon', width=60.45, distance=57)
    monitor.setSizePix([1920, 1080])
    return monitor


def configwin(mon, fullscr, screen, color):
    if fullscr:
        win = visual.Window(monitor=mon, screen=screen, units='deg',
                            pos=[0, 0], fullscr=fullscr, color=color)
    else:
        win = visual.Window(monitor=mon, units='deg',
                            size=[1200, 1000], pos=[0, 0],
                            color=color)
    win.mouseVisible = False
    return win


def test_framerate(win, nominal_fr):
    # todo: make this a real test and raise error in case of poor match
    actual_fr = win.getActualFrameRate(nIdentical=10, nMaxFrames=100,
                                       nWarmUpFrames=10, threshold=1)
    if actual_fr is not None:
        actual_fr = round(actual_fr, 2)
    print('\n=======================================================')
    print(f"Nominal frame rate:  {nominal_fr} Hz")
    print(f"Measured frame rate: {actual_fr} Hz\n")


def addfixdot(win, size=1, pos=(0, 0), color='black'):
    fixdot = visual.TextStim(win=win, text='+', height=size, pos=pos,
                             color=color)
    fixdot.draw()


def addprobe(win, radius, color, pos):
    probe = visual.Circle(win, radius=radius, fillColor=color, pos=pos)
    probe.draw()


def addsquare(win, width, color, fillcolor, pos):
    line_width = 0.1
    outer_frame = visual.Rect(win=win, size=width, fillColor=color, pos=pos)
    inner_frame = visual.Rect(win=win, size=width - line_width,
                              fillColor=fillcolor, pos=pos)
    outer_frame.draw()
    inner_frame.draw()


def gengrid(width, n, movpos1, movpos2, movsize, movdir):
    x = np.linspace(-width / 2, width / 2, n[0])
    y = np.linspace(-width / 2, width / 2, n[1])
    # move to moving object's starting position
    y = y + movpos1[1]
    # move horizontally to moving object's midway then push it back to the
    # trailing edge to give more room to the
    # more important leading edge (offset)
    offset = 1.5
    midwayx = (movpos1[0] + movpos2[0]) / 2
    if movdir == 1:
        x = x + midwayx + offset
    elif movdir == -1:
        x = x - midwayx - offset

    xv, yv = np.meshgrid(x, y)
    return xv, yv


def infoscreen(win, iblock, command_keys):
    msg = f"< Block {iblock} >" \
          f"\n\nReady to begin?"
    message = visual.TextStim(win,
                              text=msg, color='black', height=.5,
                              alignText='center')
    message.pos = (0, 0)
    message.draw()

    commands = '[Backspace]: Quit\t[0/Insert]: Begin'
    cmnd_text = visual.TextStim(win,
                                text=commands, color='black', height=.5,
                                alignText='center')
    cmnd_text.pos = (0, -2)
    cmnd_text.draw()

    win.flip()
    pressed_key = event.waitKeys(keyList=list(command_keys.values()))
    if command_keys['quit_key'] in pressed_key:
        core.quit()
    elif command_keys['response_key'] in pressed_key:
        pass
    # show a blanck window for one second
    for iframe in range(60):
        win.flip()
