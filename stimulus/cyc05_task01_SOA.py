"""
***** project: PRJ2023_MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Jan 2023

Task Procedure:
    A vertical bar starts at the center and above the fixation dot and moves
    either righward or leftward.
    A probe flashes at a distance corresponding to ~200 ms ahead of the bar.
    The bar-probe SOA varies from 0 to 700 ms in 50 ms steps.
    Each SOA repeats for 5 times.

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

subID = 'test'  # subject ID (put 'test' for a test run)
soa_arr_base_ms = np.arange(0, 750, 50)
trials_per_cnd = 5
ntrials = len(soa_arr_base_ms) * trials_per_cnd
nblocks = 3  # number of blocks

slow_coeff = 2  # on dell:1 | on mac:2

if subID == 'test':
    full_screen = False
else:
    full_screen = True
# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file name
date = sfc.get_date()
time = sfc.get_time()

output_name = f"cyc05_task01_{date}_{time}_{subID}.json"

# set data directory
save_path = os.path.join("..", "data", "cyc05", output_name)

# --------------------------------
# /// set stimulus parameters

# initialize the display and the keyboard
REF_RATE = 60

# define the flash duration in frames
frame_repeat = 2

# configure the monitor and the stimulus window
bg_color = [-.8, -.8, -.8]
mon = sfc.config_mon_macair()
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

line_start_xpos = np.arange(-1, 1.1, .1)
line_start_ypos = 4  # dva
line_end_ypos = 4  # dva

postFlashMotion_ms = 500
postFlashMotion_frame = int(postFlashMotion_ms / 1000 * REF_RATE)

motion_speed = 10  # dva/s

# npos = int(motion_dur / frame_repeat)

# randomly decide on the more likely direction
# left_bias_coeff = np.nan
# likely_dir = np.random.choice(['left', 'right'])
# if likely_dir == 'left':
#     left_bias_coeff = bias_coeff  # probability of leftward motion
# if likely_dir == 'right':
#     left_bias_coeff = 1-bias_coeff  # probability of leftward motion

# probe
probe_rad = .25
probe_color = 'red'
probe_xoffset = 2.5
probe_yoffset = 4

# potential gap durations (0.75 - 1.25 sec)
gap_durations_base = range(int(REF_RATE * .75), int(REF_RATE * 1.25) + 1, 1)

# pause trials
pause_array = np.linspace(0, ntrials, nblocks + 1)
pause_array = pause_array[:-1]

# initialize mouse
mouse = event.Mouse(win=win, visible=False)

# initialize clock
my_clock = core.Clock()

# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

soa_arr_base_frame = soa_arr_base_ms / 1000 * REF_RATE
soa_array_frame = np.repeat([soa_arr_base_frame], trials_per_cnd)

# assert ((dir_array.size == ntrials) and (probe_array.size == ntrials))

# randomize the order of each condition array
# ind_shuffle = np.arange(ntrials)
# np.random.shuffle(ind_shuffle)
# dir_array = dir_array[ind_shuffle]
# probe_array = probe_array[ind_shuffle]

# ----------------------------------------------------------------------------
# /// CREATE VISUAL OBJECTS ///

# line
vline = visual.Rect(win=win,
                    size=(line_width, vline_length),
                    fillColor=line_color)

# probe
# probe = visual.Circle(win,
#                       radius=probe_rad,
#                       pos=(probe_array[itrial], probe_yoffset),
#                       fillColor=probe_color)

# fixation dot
fixdot1 = visual.Circle(win,
                        radius=fixdot_radius,
                        pos=(FIX_X, FIX_Y),
                        fillColor=fixdot_color)
fixdot2 = visual.Circle(win,
                        radius=fixdot_radius * .7,
                        pos=(FIX_X, FIX_Y),
                        fillColor=bg_color)

# ----------------------------------------------------------------------------
# /// TRIAL BEGINS ///

for itrial in range(ntrials):

    # --------------------------------
    # /// resets

    # reset mouse position
    mouse.setPos((0, 0))
    mouse.setVisible(False)

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    iti = np.random.choice(gap_durations_base)
    postFixGap = np.random.choice(gap_durations_base)
    soa = int(soa_array_frame[itrial])
    motion_dur_frames = soa + postFlashMotion_frame
    motion_dir = np.random.choice([-1, 1])
    xshift_steps = motion_speed / REF_RATE * frame_repeat

    # --------------------------------
    # print('---------------------------')
    # print(f'trial number    : {itrial + 1}')
    # print(f'likely direction: {likely_dir}')
    # print(f'motion direction: {dir_array[itrial]}')

    # --------------------------------
    # /// create motion trajectory array
    line_end_xpos = (motion_dur_frames * xshift_steps) + \
                    line_start_xpos[itrial]

    motionX_array = np.linspace(line_start_xpos[itrial],
                                line_end_xpos * motion_dir,
                                num=motion_dur_frames)
    motionY_array = np.linspace(line_start_ypos,
                                line_end_ypos,
                                num=motion_dur_frames)

    motionX_array = np.repeat(motionX_array, frame_repeat)
    motionY_array = np.repeat(motionY_array, frame_repeat)

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

    # my_clock.reset()
    # motion_dur = npos * frame_repeat

    # move the vertical bar & flash the probe
    for i in range(len(motionX_array)):
        for islow in range(slow_coeff):
            vline.pos = (motionX_array[i], motionY_array[i])
            vline.draw()

            # flash the probe
            # if icount == 0:
            #     probe.draw()

            win.flip()

    motion_dur_measured = round(my_clock.getTime(), 2)
    # print(f'Motion duration : {motion_dur_measured} s')
    #
    click_pos = np.round(get_mouseclick(win), 2)
    # click_err = np.round(click_pos - probe.pos, 2)
    # print(f'probe position  : {probe.pos} dva')
    # print(f'click position  : {click_pos} dva')
    # print(f'click error     : {click_err} dva')
    print(f'motion duration " {motion_dur_measured} ms')

    # --------------------------------
    # /// prepare data for saving

    # # create a dictionary of variables to be saved
    # trial_dict = {'trial_num': itrial + 1,
    #               'likely_dir': likely_dir,
    #               'bar_dir': dir_array[itrial],
    #               'probe_pos': [probe.pos],
    #               'click_pos': [click_pos],
    #               'click_err': [click_err],
    #               'click_xerr': [click_err[0]],
    #               'click_yerr': [click_err[1]]}
    #
    # # convert to data frame
    # dfnew = pd.DataFrame(trial_dict)
    # # if not first trial, load the existing data frame and concatenate
    # if itrial > 0:
    #     df = pd.read_json(save_path)
    #     dfnew = pd.concat([df, dfnew], ignore_index=True)
    # # save the dataframe
    # dfnew.to_json(save_path)
    #
    # if itrial == ntrials - 1:
    #     sfc.end_screen(win, color='white')
# --------------------------------
win.close()
