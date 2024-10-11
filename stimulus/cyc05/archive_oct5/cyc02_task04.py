"""
***** project: PRJ2023_MIPS-Attention *****

    Mo Shams <MShamsCBR@gmail.com>
    Sep 19, 2023


Task Procedure:
    Two dots flash in an oblique pattern
    Then two vertical bars flash
    Subject adjusts the the two bars so that they appear vertically aligned

There are two direction conditions:
    d = -1: flashes make a positive angle diagonal
    d = +1: flashes make a negative angle diagonal

"""

import os
import random
import warnings
import numpy as np
import pandas as pd
from lib import stim_flow_control as sfc
from psychopy import event, visual, core


def check_pressed_keys():
    pressed_key_f = event.getKeys(keyList=['space', 'escape'])
    if 'escape' in pressed_key_f:
        core.quit()
    if 'space' in pressed_key_f or 'escape' in pressed_key_f:
        fixdot.color = 'green'
        fixdot.size = fixdot.size * 2
        for iiframe_f in range(REF_RATE):
            fixdot.draw()
            win.flip()
        return True
    else:
        return False


# disable Panda's false warning message
pd.options.mode.chained_assignment = None  # default='warn'

# ----------------------------------------------------------------------------

# /// INSERT SESSION'S META DATA ///

subID = "test"
N_DIR = 2
N_REP = 6  # repetition of each contrast (min = 2; has to be Even)
N_TRIALS = N_DIR * N_REP
full_screen = False  # (True/False)
# ----------------------------------------------------------------------------

# /// CONFIGURE LOAD/SAVE FILES & DIRECTORIES ///

# create file nameTrue
date = sfc.get_date()
time = sfc.get_time()
output_name = f"{subID}_task04_{date}_{time}.json"
# set data directory
save_path = os.path.join("../..", "data", "cyc02", output_name)
# ----------------------------------------------------------------------------

# /// CONFIGURE STIMULUS PARAMETERS AND INPUTS ///

# initialize the display and the keyboard
REF_RATE = 60

# define the flash duration in frames
frame_repeat = 2

# configure the monitor and the stimulus window
mon = sfc.config_mon_dell()
if not full_screen:
    win = visual.Window(monitor=mon,
                        units='deg',
                        pos=[0, 0],
                        size=[1920, 700],
                        color=[0, 0, 0])
else:
    win = visual.Window(monitor=mon,
                        units='deg',
                        pos=[0, 0],
                        fullscr=full_screen,
                        color=[0, 0, 0])

sfc.test_refresh_rate(win, REF_RATE)

# fixation cross
FIX_SIZE = .35
FIX_X = 0
FIX_Y = 0

INSTRUCT_DUR = REF_RATE  # duration of the instruction period [frames]

# horizontal offset of the discs and the bars [deg]
yoffset = 3

# disc size [deg]
disc_rad = .5
disc_xoffset_base = .5
disc_dur = 50  # [ms]
disc_color = 'black'

# probe lines [deg]
line_width = 0.2
line_length = .7
line1_color = 'crimson'
line2_color = 'blue'
line_dur = 20  # [ms]

flash2bar_gap_dur = 100  # [ms]

# mouse position downsample factor
mouse_dsf = 10

# potential gap durations (2 to 3 sec)
gap_dur_list = range(int(REF_RATE * 2), int(REF_RATE * 3) + 1, 1)

# potential fixation durations (2 to 3 sec)
fix_dur_list = range(int(REF_RATE * 2), int(REF_RATE * 3) + 1, 1)

# show a message before the block begins
# sfc.block_msg(win, iblock, N_BLOCKS, command_keys)

# initialize mouse
mouse = event.Mouse(win=win, visible=False)

# create an equal number of trials per condition (contrast/direction)
dir_array = np.repeat([-1, 1], N_REP)

# randomize the order of the condition array
cnd_ind_arr = np.arange(dir_array.shape[0])
np.random.shuffle(cnd_ind_arr)
dir_array = dir_array[cnd_ind_arr]

# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# ----------------------------------------------------------------------------

# /// TRIAL BEGINS ///

for itrial in range(N_TRIALS):

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    # randomly decide on gap duration
    gap_dur = random.choice(gap_dur_list)

    # reset mouse position
    mouse.setPos((0, 0))

    # --------------------------------
    # /// run the stimulus

    hline_x = np.nan
    pressed_key = []

    # add random offset to hline's horizontal onset position
    # line_x_offset = np.random.choice(np.arange(-1, 1, 0.1))
    line_x_offset = 0

    # adjust flash diagonal angle
    if dir_array[itrial] == -1:
        disc_xoffset = -disc_xoffset_base
    else:
        disc_xoffset = disc_xoffset_base
    # gap period
    for igap in range(gap_dur):
        win.flip()

    loop_flag = True

    fixdot = visual.TextStim(win=win,
                             text='o',
                             height=FIX_SIZE,
                             pos=(FIX_X, FIX_Y),
                             color='black')

    disc1 = visual.Circle(win, radius=disc_rad, fillColor=disc_color,
                          pos=(disc_xoffset, yoffset))
    disc2 = visual.Circle(win, radius=disc_rad, fillColor=disc_color,
                          pos=(-disc_xoffset, -yoffset))

    line1 = visual.Rect(win,
                        width=line_width,
                        height=line_length,
                        pos=(line_x_offset, -yoffset),
                        fillColor=line1_color)
    line2 = visual.Rect(win,
                        width=line_width,
                        height=line_length,
                        pos=(-line_x_offset, yoffset),
                        fillColor=line2_color)

    print('---------------------------')
    print(f'trial: {itrial + 1}')
    print(f'direction: {dir_array[itrial]}')

    while loop_flag:

        # randomly decide on fixation duration
        fix_dur = random.choice(fix_dur_list)

        # get mouse x-position
        line_x = mouse.getPos()[0] / mouse_dsf + line_x_offset

        if loop_flag:
            # fixation period
            for iframe in range(fix_dur):
                if check_pressed_keys():
                    loop_flag = False
                    break
                fixdot.draw()
                win.flip()

        if loop_flag:
            # flash discs
            for iframe in range(int(disc_dur / 1000 * REF_RATE)):
                if check_pressed_keys():
                    loop_flag = False
                    break
                fixdot.draw()
                disc1.draw()
                disc2.draw()
                win.flip()

        if loop_flag:
            # pause
            for iframe in range(int(flash2bar_gap_dur / 1000 * REF_RATE)):
                if check_pressed_keys():
                    loop_flag = False
                    break
                fixdot.draw()
                win.flip()

        if loop_flag:
            # flash bars
            for iframe in range(int(line_dur / 1000 * REF_RATE)):
                if check_pressed_keys():
                    fixdot.color = 'green'
                    fixdot.size = fixdot.size * 2
                    for iiframe in range(REF_RATE):
                        fixdot.draw()
                        win.flip()
                    loop_flag = False
                    break
                # set pos and draw horizontal line
                line1.pos = line_x, yoffset
                line2.pos = -line_x, -yoffset
                line1.draw()
                line2.draw()
                win.flip()

    print(f'PSE: {np.round(line_x, 2)}')

    # --------------------------------

    # /// prepare data for saving

    # create a dictionary of variables to be saved
    trial_dict = {'trial_num': itrial + 1,
                  'direction': dir_array[itrial],
                  'pse_x': [np.round(line_x, 2)]}

    # convert to data frame
    dfnew = pd.DataFrame(trial_dict)
    # if not first trial, load the existing data frame and concatenate
    if itrial > 0:
        df = pd.read_json(save_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
    # save the dataframe
    dfnew.to_json(save_path)
# --------------------------------

win.close()
