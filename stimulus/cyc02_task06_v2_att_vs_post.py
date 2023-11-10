"""
***** project: MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Oct 2023

Task Procedure:
    A '|""|' like shape moves downward toward center, a probe flashes,
    then the shape continues to move either rightward or leftward. The
    probability of leftward motion trials (bias_factor) can be set for
    each session.

There are two post-flash direction conditions:
    dir = 'l': leftward motion
    dir = 'r': rightward motion

"""

import os
import random
import warnings
import numpy as np
import pandas as pd
from lib import stim_flow_control as sfc
from psychopy import event, visual, core


def get_mouseclick(win, ms_corrcoef=1):
    ms_posx = random.choice(range(-2, 2 + 1))
    ms_posy = random.choice(range(-2, 2 + 1))
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

subID = 'NN01'
nrep = 50
ndir = 2
ntrs = nrep * ndir
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
output_name = f"{subID}_task06_v2_fair_{date}_{time}.json"
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

# lines
line_width = 0.12
hline_length = 2
vline_length = 1.2
line_color = 'black'
line_offset = 0

motion_cycle_dur = REF_RATE  # [frames]
preflash_dist = 5  # dva
postflash_dist = 5  # dva
npos = int(motion_cycle_dur / frame_repeat / 2)
bias_factor = 0.5  # probability of leftward post-flash motion

# probe
probe_rad = .15
probe_color = 'red'
probe_pos = (0, 1)

# potential gap durations (0.5 to 1 sec)
gap_dur_list = range(int(REF_RATE / 2), int(REF_RATE / 1) + 1, 1)

# initialize mouse
mouse = event.Mouse(win=win, visible=False)

# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

# create an equal number of trials per condition (contrast/direction)
dir_array = np.repeat([-1, 1], [int(round(ntrs * bias_factor)),
                                int(round(ntrs * (1 - bias_factor)))])

assert (dir_array.size == ntrs)

# randomize the order of each condition array
ind_shuffle = np.arange(ntrs)
np.random.shuffle(ind_shuffle)
dir_array = dir_array[ind_shuffle]

# pause trials
pause_array = np.linspace(0, ntrs, nblocks + 1)
pause_array = pause_array[:-1]

# ----------------------------------------------------------------------------
# /// TRIAL BEGINS ///

for itrial in range(ntrs):
    # --------------------------------
    # /// resets

    # reset mouse position
    mouse.setPos(probe_pos)
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
    print(f'stm: {dir_array[itrial]}')

    # --------------------------------
    # /// create visual objects

    # lines
    hline = visual.Rect(win=win,
                        size=(hline_length, line_width),
                        fillColor=line_color)
    vlineL = visual.Rect(win=win,
                         size=(line_width, vline_length),
                         fillColor=line_color)
    vlineR = visual.Rect(win=win,
                         size=(line_width, vline_length),
                         fillColor=line_color)

    # probe
    probe = visual.Circle(win,
                          radius=probe_rad,
                          pos=probe_pos,
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

    motion1x_array = np.linspace(probe_pos[0], probe_pos[0], num=npos)
    motion1y_array = np.linspace(preflash_dist, probe_pos[1], num=npos)

    motion2x_array = np.linspace(probe_pos[0],
                                 dir_array[itrial] * postflash_dist, num=npos)
    motion2y_array = np.linspace(probe_pos[1], probe_pos[1], num=npos)

    motionx_array = np.concatenate((motion1x_array, motion2x_array))
    motiony_array = np.concatenate((motion1y_array, motion2y_array))

    motionx_array = np.repeat(motionx_array, frame_repeat)
    motiony_array = np.repeat(motiony_array, frame_repeat) + line_offset

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
        vlineL.pos = (motionx_array[i] - hline_length / 2,
                      motiony_array[i])
        vlineR.pos = (motionx_array[i] + hline_length / 2,
                      motiony_array[i])
        hline.pos = (motionx_array[i],
                     motiony_array[i] + vline_length / 2)
        vlineL.draw()
        vlineR.draw()
        hline.draw()

        # fixdot1.draw()
        # fixdot2.draw()

        if hline.pos[0] == probe_pos[0] and vlineL.pos[1] == probe_pos[1]:
            probe.draw()

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
                  'postflash_dir': dir_array[itrial],
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
