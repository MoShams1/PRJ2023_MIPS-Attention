import math
import numpy as np
from datetime import date, datetime
from psychopy import monitors, visual, event, core


def test_refresh_rate(win, ref_rate):
    # measure the actual frame rate
    actual_fr = win.getActualFrameRate(nIdentical=10,
                                       nMaxFrames=100,
                                       nWarmUpFrames=10,
                                       threshold=1)
    if actual_fr is not None:
        actual_fr = round(actual_fr, 2)

    print('\n=======================================================')
    print(f"Nominal refresh rate:  {ref_rate} Hz")
    print(f"Measured refresh rate: {actual_fr} Hz\n")


def config_mon_imac24():
    monitor = monitors.Monitor('prim_mon', width=54.7, distance=57)
    monitor.setSizePix([2240, 1260])
    return monitor


def config_mon_macair():
    monitor = monitors.Monitor('prim_mon', width=33.78, distance=57)
    monitor.setSizePix([1440, 900])
    return monitor


def config_mon_dell():
    monitor = monitors.Monitor('prim_mon', width=52, distance=70)
    monitor.setSizePix([1920, 1080])
    return monitor


def config_win(mon, fullscr, screen=0, color=(0, 0, 0)):
    if fullscr:
        win = visual.Window(monitor=mon,
                            screen=screen,
                            units='deg',
                            pos=[0, 0],
                            fullscr=fullscr,
                            color=color)
    else:
        win = visual.Window(monitor=mon,
                            units='deg',
                            size=[1920, 700],
                            pos=[0, 0],
                            color=color)
    win.mouseVisible = False
    return win


def draw_fixdot(win, size, pos):
    fix_marker = 'o'
    fixdot = visual.TextStim(win=win,
                             text=fix_marker,
                             height=size,
                             pos=pos,
                             color='black')
    fixdot.draw()


def draw_probe(win, color, radius=.5, pos=(0, 0)):
    inner_probe = visual.Circle(win,
                                radius=radius,
                                fillColor=color,
                                pos=pos)
    inner_probe.draw()


def get_date():
    today = date.today()
    return (str(today.year).zfill(4) +
            str(today.month).zfill(2) +
            str(today.day).zfill(2))


def get_time():
    now = datetime.now()
    return now.strftime("%H%M%S")


def block_msg(win, iblock, nblocks, command_keys):
    msg = f"<<< Block {iblock} / {nblocks} >>>" \
          f"\n\nPlease respond as quickly as possible!" \
          f"\nRED <---   O   ---> BLUE" \
          f"\n\nReady to begin?"
    message = visual.TextStim(win,
                              text=msg,
                              color='black',
                              height=.5,
                              alignText='center')
    message.pos = (0, 0)
    message.draw()

    commands = '\n\n[Escape]: Quit\t\t[Spacebar]: Begin'
    cmnd_text = visual.TextStim(win,
                                text=commands,
                                color='black',
                                height=.5,
                                alignText='center')
    cmnd_text.pos = (0, -2)
    cmnd_text.draw()

    win.flip()

    pressed_key = event.waitKeys(keyList=["escape", "space"])
    if pressed_key[0] in command_keys['quit_key']:
        core.quit()
    if pressed_key[0] in ["space"]:
        pass

    # show a blanck window for one second
    for iframe in range(60):
        win.flip()


def block_msg2(win, iblock, nblocks, color='black'):
    msg = f"<<< Block {iblock} / {nblocks} >>>" \
          f"\n\nPlease inform the experimenter before you continue..."
    message = visual.TextStim(win,
                              text=msg,
                              color=color,
                              height=.5,
                              alignText='center',
                              pos=(0, 0))

    commands = '\n\n[Escape]: Quit\t\t[Spacebar]: Continue'
    cmnd_text = visual.TextStim(win,
                                text=commands,
                                color=color,
                                height=.5,
                                alignText='center',
                                pos=(0, -2))

    message.draw()
    cmnd_text.draw()
    win.flip()

    pressed_key = event.waitKeys(keyList=['escape', 'space'])
    if pressed_key[0] == 'escape':
        core.quit()
    if pressed_key[0] == 'space':
        pass


def block_msg3(win, iblock, nblocks, color='black'):
    msg = f"<<< Block {iblock} / {nblocks} >>>" \
          f"\n\nPlease continue when ready..."
    message = visual.TextStim(win,
                              text=msg,
                              color=color,
                              height=.5,
                              alignText='center',
                              pos=(0, 0))

    commands = '\n\n[Escape]: Quit\t\t[Spacebar]: Continue'
    cmnd_text = visual.TextStim(win,
                                text=commands,
                                color=color,
                                height=.5,
                                alignText='center',
                                pos=(0, -2))

    message.draw()
    cmnd_text.draw()
    win.flip()

    pressed_key = event.waitKeys(keyList=['escape', 'space'])
    if pressed_key[0] == 'escape':
        core.quit()
    if pressed_key[0] == 'space':
        pass


def decide_on_show(iframe, nframes):
    # iframe: current frame number
    # nframes: number of frames as the image interval
    iactive = math.ceil(nframes // 2)  # show the img during half of the
    # interval
    index = iframe % nframes  # calculate where we are now in the interval
    # decide whether to show or not to show the image
    if index < iactive:
        return True
    else:
        return False


def cal_next_tilt(goal_perf, run_perf):
    delta = goal_perf - run_perf
    delta_max = max([100 - goal_perf, goal_perf])
    step_max = 5
    step_change = round(delta / delta_max * step_max, 0)
    return step_change


def gen_image_pairs(nexmp, ntrials):
    face_cntr = np.repeat(np.arange(1, nexmp + 1, 1), nexmp)
    house_cntr = np.tile(np.arange(1, nexmp + 1, 1), nexmp)
    allpairs = np.array(list(zip(face_cntr, house_cntr)))
    np.random.shuffle(allpairs)
    pairs = allpairs[:ntrials]
    return pairs


def end_screen(win, color='black'):
    msg = 'Experiment finished successfully.\n Thank you!'
    message = visual.TextStim(win,
                              text=msg,
                              color=color,
                              height=.65,
                              alignText='center',
                              pos=(0, 0))
    for i in range(3 * 60):
        message.draw()
        win.flip()
