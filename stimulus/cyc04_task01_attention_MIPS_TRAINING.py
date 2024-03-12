"""
***** project: MIPS-Attention (TRAINING)

    Mohammad Shams <m.shams.ahmar@gmail.com>
    March 2023

Task Procedure:
    A vertical bar starts at the center and above the fixation dot and moves
    either righward or leftward.
    A probe flashes at a distance corresponding to ~200 ms away from the
    bar, either ahead or behind it.
    The expected direction is set randomly for each subject.

There are four conditions:
    - Expected direction & flash ahead (att. repulsion + sweep)
    - Unexpected direction & flash ahead (sweep)
    - Unexpected direction & flash behind (att. repulsion)
    - Expected direction & flash behind

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

subID = 'training'  # subject ID (put 'test' for a test run)
ntrs = 300  # number of all trials
nblocks = 4  # number of blocks
bias_coeff = .5  # probability of more likely direction

slow_coeff = 1  # on dell:1 | on mac:2

if subID == 'test':
    full_screen = False
else:
    full_screen = True
# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file name
date = sfc.get_date()
time = sfc.get_time()

output_name = f"cyc04_task01_{date}_{time}_{subID}.json"

# set data directory
save_path = os.path.join("..", "data", "cyc04", output_name)

# --------------------------------
# /// set stimulus parameters

# initialize the display and the keyboard
REF_RATE = 60

# define the flash duration in frames
frame_repeat = 2

# configure the monitor and the stimulus window
bg_color = [-.8, -.8, -.8]
mon = sfc.config_mon_dell()
win = sfc.config_win(mon=mon, fullscr=full_screen, color=bg_color)
sfc.test_refresh_rate(win, REF_RATE)

# fixation mark
fixdot_radius = .16
FIX_X = 0
FIX_Y = -2
fixdot_color = 'white'

# lines
line_width = 0.2
vline_length = 2
line_color = 'white'

line_start_pos = (0, 4)  # dva
line_end_offset = 10  # dva

motion_dur = REF_RATE  # [frames]
npos = int(motion_dur / frame_repeat)

# randomly decide on the more likely direction
left_bias_coeff = np.nan
likely_dir = np.random.choice(['left', 'right'])
if likely_dir == 'left':
    left_bias_coeff = bias_coeff  # probability of leftward motion
if likely_dir == 'right':
    left_bias_coeff = 1-bias_coeff  # probability of leftward motion

# probe
probe_rad = .25
probe_color = 'red'
probe_xoffset = 2.5
probe_yoffset = line_start_pos[1]

# potential gap durations (0.75 - 1.25 sec)
gap_dur_list = range(int(REF_RATE * .75), int(REF_RATE * 1.25) + 1, 1)

# initialize mouse
mouse = event.Mouse(win=win, visible=False)

# initialize clock
my_clock = core.Clock()

# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

# calculate number of leftward and rightward motion trials
nleft = int(round(ntrs * left_bias_coeff))
nright = int(round(ntrs * (1 - left_bias_coeff)))
# create an equal number of trials per condition (contrast/direction)
dir_array = np.repeat([-1, 1], [nleft, nright])
# create an equal number of probe positions for each direction
probe_array1 = np.repeat([-probe_xoffset, probe_xoffset],
                         [nleft / 2, nleft / 2])
probe_array2 = np.repeat([-probe_xoffset, probe_xoffset],
                         [nright / 2, nright / 2])
probe_array = np.concatenate((probe_array1, probe_array2))

assert ((dir_array.size == ntrs) and (probe_array.size == ntrs))

# randomize the order of each condition array
ind_shuffle = np.arange(ntrs)
np.random.shuffle(ind_shuffle)
dir_array = dir_array[ind_shuffle]
probe_array = probe_array[ind_shuffle]

# pause trials
pause_array = np.linspace(0, ntrs, nblocks + 1)
pause_array = pause_array[:-1]

# ----------------------------------------------------------------------------
# /// TRIAL BEGINS ///

for itrial in range(ntrs):

    # --------------------------------
    # /// resets

    # reset mouse position
    mouse.setPos((0, 0))
    mouse.setVisible(False)

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    # randomly decide on inter-trial interval
    iti = random.choice(gap_dur_list)
    postFixGap = random.choice(gap_dur_list)

    # --------------------------------
    print('---------------------------')
    print(f'trial number    : {itrial + 1}')
    print(f'likely direction: {likely_dir}')
    print(f'motion direction: {dir_array[itrial]}')

    # --------------------------------
    # /// create visual objects

    # line
    vline = visual.Rect(win=win,
                        size=(line_width, vline_length),
                        fillColor=line_color)

    # probe
    probe = visual.Circle(win,
                          radius=probe_rad,
                          pos=(probe_array[itrial], probe_yoffset),
                          fillColor=probe_color)

    # fixation dot
    fixdot1 = visual.Circle(win,
                            radius=fixdot_radius,
                            pos=(FIX_X, FIX_Y),
                            fillColor=fixdot_color)
    fixdot2 = visual.Circle(win,
                            radius=fixdot_radius * .7,
                            pos=(FIX_X, FIX_Y),
                            fillColor=bg_color)

    # --------------------------------
    # /// create motion trajectory array

    motionx_array = np.linspace(line_start_pos[0],
                                dir_array[itrial] * line_end_offset,
                                num=npos)
    motiony_array = np.linspace(line_start_pos[1],
                                line_start_pos[1],
                                num=npos)

    motionx_array = np.repeat(motionx_array, frame_repeat)
    motiony_array = np.repeat(motiony_array, frame_repeat)

    # --------------------------------
    # /// run stimulus

    # show the block screeen
    if itrial in pause_array:
        sfc.block_msg2(win, np.where(pause_array == itrial)[0][0] + 1,
                       nblocks, color='white')

    # inter-trial interval gap period
    for igap in range(iti):
        win.flip()

    # fixation period
    for ifix in range(REF_RATE):
        fixdot1.draw()
        fixdot2.draw()
        win.flip()

    # post-fixation gap period
    for ifix in range(postFixGap):
        win.flip()

    my_clock.reset()
    motion_dur = npos * frame_repeat

    # move the vertical bar & flash the probe
    for i, icount in enumerate(range(motion_dur)):
        for islow in range(slow_coeff):
            vline.pos = (motionx_array[i], motiony_array[i])
            vline.draw()

            # flash the probe
            if icount == 0:
                probe.draw()

            win.flip()

    motion_dur_measured = round(my_clock.getTime(), 2)
    print(f'Motion duration : {motion_dur_measured} s')

    click_pos = np.round(get_mouseclick(win), 2)
    click_err = np.round(click_pos - probe.pos, 2)
    print(f'probe position  : {probe.pos} dva')
    print(f'click position  : {click_pos} dva')
    print(f'click error     : {click_err} dva')

    # --------------------------------

    if itrial == ntrs - 1:
        sfc.end_screen(win, color='white')
# --------------------------------
win.close()
