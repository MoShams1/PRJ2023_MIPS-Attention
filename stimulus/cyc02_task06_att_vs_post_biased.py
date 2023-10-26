"""
***** project: MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Oct 2023

Task Procedure:
    A '|__' like shape moves from bottom toward center, a probe flashes,
    then the shape continues to move either horizontally (80%) or vertically
    (20%).

There are two pre-flash direction conditions:
    dir1 = +1: rightward and upward motion
    dir1 = -1: leftward and upward motion

There are two post-flash direction conditions:
    dir2 = 'h': horizontal motion
    dir2 = 'v': vertical motion

"""

import os
import random
import warnings
import numpy as np
import pandas as pd
from lib import stim_flow_control as sfc
from psychopy import event, visual, core


def get_mouseclick(win, ms_corrcoef=1):
    ms_posx = random.choice(range(-3, 3 + 1))
    ms_posy = random.choice(range(-3, 3 + 1))
    mouse = event.Mouse(win=win, visible=True,
                        newPos=[ms_posx * ms_corrcoef,
                                ms_posy * ms_corrcoef])
    while not mouse.getPressed()[0]:
        escape_session()  # force exit with 'escape' button
        win.flip()
    while mouse.getPressed()[0]:
        pass
    click_loc = mouse.getPos() / ms_corrcoef
    click_loc = [round(item, 2) for item in click_loc]
    return click_loc


def escape_session():
    exit_key = event.getKeys(keyList=['escape'])
    if 'escape' in exit_key:
        core.quit()


# disable Panda's false warning message
pd.options.mode.chained_assignment = None  # default='warn'

# ----------------------------------------------------------------------------
# /// INSERT SESSION'S META DATA ///

subID = 'test'
nrep = 10
ndir1 = 2
ndir2 = 5
ntrs = nrep * ndir1 * ndir2
nblocks = 4

if subID == 'test':
    full_screen = False
else:
    full_screen = True
# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file nameTrue
date = sfc.get_date()
time = sfc.get_time()
output_name = f"{subID}_task06_{date}_{time}.json"
# set data directory
save_path = os.path.join("..", "data", "cyc02", output_name)

# --------------------------------
# /// set stimulus parameters

# initialize the display and the keyboard
REF_RATE = 60

# define the flash duration in frames
frame_repeat = 2

# configure the monitor and the stimulus window
mon = sfc.config_mon_dell()
win = sfc.config_win(mon=mon, fullscr=full_screen)
sfc.test_refresh_rate(win, REF_RATE)

# fixation mark
fixdot_radius = .16
FIX_X = 0
FIX_Y = -2
fixdot_color = 'black'

INSTRUCT_DUR = REF_RATE  # duration of the instruction period [frames]

# lines
line_width = 0.12
line_length = 2
line_color = 'black'
voffset = 1

motion_cycle_dur = REF_RATE  # [frames]
leg_dist = 8  # dva
npos = int(REF_RATE / frame_repeat / 2)

# probe
probe_rad = .15
probe_color = 'red'

# potential gap durations (0.5 to 1 sec)
gap_dur_list = range(int(REF_RATE / 2), int(REF_RATE / 1) + 1, 1)

# initialize mouse
mouse = event.Mouse(win=win, visible=False)

# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

# create an equal number of trials per condition (contrast/direction)
dir2_array = np.repeat(['h', 'h', 'h', 'h', 'v'], ntrs / 5)
assert (dir2_array.size == ntrs)
dir1_array = np.tile(np.repeat([-1, 1], int(ntrs / 10)), 5)
assert (dir1_array.size == ntrs)

# randomize the order of each condition array
ind_shuffle = np.arange(ntrs)
np.random.shuffle(ind_shuffle)
dir2_array = dir2_array[ind_shuffle]
dir1_array = dir1_array[ind_shuffle]

# pause trials
pause_array = np.linspace(0, ntrs, nblocks + 1)
pause_array = pause_array[:-1]

# ----------------------------------------------------------------------------
# /// TRIAL BEGINS ///

for itrial in range(ntrs):
    # --------------------------------
    # /// resets

    motionx1_array = None
    motionx2_array = None
    motiony1_array = None
    motiony2_array = None

    # reset mouse position
    mouse.setPos((0, 0))
    mouse.setVisible(False)

    # reset pse response
    hline_x = np.nan

    # reset loop counter
    loop_cntr = 0

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    # randomly decide on inter-trial interval
    iti = random.choice(gap_dur_list)

    # --------------------------------
    print('---------------------------')
    print(f'trl: {itrial + 1}')
    print(f'stm: {dir1_array[itrial]}')
    print(f'dir: {dir2_array[itrial]}')

    # --------------------------------
    # /// create visual objects

    # lines
    vline = visual.Rect(win=win,
                        size=(line_width, line_length),
                        fillColor=line_color)
    hline = visual.Rect(win=win,
                        size=(line_length, line_width),
                        fillColor=line_color)
    # probe
    probe = visual.Circle(win,
                          radius=probe_rad,
                          pos=(0, voffset),
                          fillColor=probe_color)
    # fixation dot
    fixdot1 = visual.Circle(win,
                            radius=fixdot_radius,
                            pos=(FIX_X, FIX_Y),
                            fillColor=fixdot_color)
    fixdot2 = visual.Circle(win,
                            radius=fixdot_radius * .7,
                            pos=(FIX_X, FIX_Y),
                            fillColor='gray')

    # --------------------------------
    # /// create motion arrays

    if dir1_array[itrial] == 1:
        motionx1_array = np.linspace(-leg_dist, 0, num=npos) / np.sqrt(2)
        motiony1_array = np.linspace(-leg_dist, 0, num=npos) / np.sqrt(2)
        if dir2_array[itrial] == 'h':
            motionx2_array = np.linspace(0, leg_dist, num=npos)
            motiony2_array = np.linspace(0, 0, num=npos)
        if dir2_array[itrial] == 'v':
            motionx2_array = np.linspace(0, 0, num=npos)
            motiony2_array = np.linspace(0, leg_dist, num=npos)
    if dir1_array[itrial] == -1:
        motionx1_array = np.linspace(leg_dist, 0, num=npos) / np.sqrt(2)
        motiony1_array = np.linspace(-leg_dist, 0, num=npos) / np.sqrt(2)
        if dir2_array[itrial] == 'h':
            motionx2_array = np.linspace(0, -leg_dist, num=npos)
            motiony2_array = np.linspace(0, 0, num=npos)
        if dir2_array[itrial] == 'v':
            motionx2_array = np.linspace(0, 0, num=npos)
            motiony2_array = np.linspace(0, leg_dist, num=npos)

    motionx_array = np.concatenate((motionx1_array, motionx2_array))
    motiony_array = np.concatenate((motiony1_array, motiony2_array))

    motionx_array = np.repeat(motionx_array, frame_repeat)
    motiony_array = np.repeat(motiony_array, frame_repeat) + voffset

    # --------------------------------
    # /// run the stimulus

    if itrial in pause_array:
        sfc.block_msg2(win, np.where(pause_array == itrial)[0][0] + 1, nblocks)

    # gap period
    for igap in range(iti):
        win.flip()

    # fixation period
    for ifix in range(REF_RATE):
        fixdot1.draw()
        fixdot2.draw()
        win.flip()

    # gap period
    for ifix in range(
            int(np.random.choice(np.arange(REF_RATE / 2, REF_RATE)))):
        win.flip()

    for i in range(npos * frame_repeat * 2):
        vline.pos = (motionx_array[i] - dir1_array[itrial] * line_length / 2,
                     motiony_array[i])
        hline.pos = (motionx_array[i],
                     motiony_array[i] - line_length / 2)
        vline.draw()
        hline.draw()

        if hline.pos[0] == 0 and vline.pos[1] == voffset:
            probe.draw()

            # for ii in range(120):
            #     probe.draw()
            #     vline.draw()
            #     hline.draw()
            #     win.flip()

        win.flip()

    click_pos = get_mouseclick(win)
    click_err = click_pos - probe.pos
    print(f'probe pos: {probe.pos}')
    print(f'click pos: {click_pos}')
    print(f'click err: {click_err}')

    # --------------------------------
    # /// prepare data for saving

    # create a dictionary of variables to be saved
    trial_dict = {'trial_num': itrial + 1,
                  'preflash_dir': dir1_array[itrial],
                  'postflash_dir': dir2_array[itrial],
                  'probe_pos': [probe.pos],
                  'click_pos': [click_pos],
                  'click_err': [click_err],
                  'click_xerr': [click_err[0]],
                  'click_yerr': [click_err[1]]}

    # convert to data frame
    dfnew = pd.DataFrame(trial_dict)
    # if not first trial, load the existing data frame and concatenate
    if itrial > 0:
        df = pd.read_json(save_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
    # save the dataframe
    dfnew.to_json(save_path)

    if itrial == ntrs - 1:
        sfc.end_screen(win)
# --------------------------------
win.close()
