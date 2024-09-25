"""
***** project: PRJ2023_MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Sep 2024

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
soa_arr_base_ms = np.arange(-700, -500, 50)
trials_per_cnd = 5  # todo: update this
ntrials = len(soa_arr_base_ms) * trials_per_cnd
nblocks = 3  # number of blocks #todo: update this

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

# probe
probe_rad = .25
probe_color = 'red'
probe2bar_ms = 500  # todo: vary this pseudo-randomly [-250, 250, 500]
# todo: vary the variable below pseudo-randomly [-1.5, 0, 1.5]
# There will be (15 SOA) x (3 probe2bar) x (3 probe_x) = 135
# (135 cnd) x (2 rep) = 270 trials
# (270 trials) x (5 sec) = 1350 sec = 22.5 min
probe_xoffset_base = np.arange(-1.5, 1.5+.1, .1)
probe_yoffset = 4

# lines
line_width = 0.2
vline_length = 2
line_color = 'white'
line_vel = 10  # dva/s

line_start_ypos = 4  # dva
line_end_ypos = 4  # dva

postFlashMotion_ms = 500
postFlashMotion_frame = int(postFlashMotion_ms / 1000 * REF_RATE)

# npos = int(motion_dur / frame_repeat)

# randomly decide on the more likely direction
# left_bias_coeff = np.nan
# likely_dir = np.random.choice(['left', 'right'])
# if likely_dir == 'left':
#     left_bias_coeff = bias_coeff  # probability of leftward motion
# if likely_dir == 'right':
#     left_bias_coeff = 1-bias_coeff  # probability of leftward motion

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

soa_array_ms = np.repeat([soa_arr_base_ms], trials_per_cnd)
np.random.shuffle(soa_array_ms)

# soa_arr_base_frame = soa_arr_base_ms / 1000 * REF_RATE
# soa_array_frame = np.repeat([soa_arr_base_frame], trials_per_cnd)
# np.random.shuffle(soa_array_frame)

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
probe = visual.Circle(win,
                      radius=probe_rad,
                      pos=[0, 0],
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
    soa_ms = int(soa_array_ms[itrial])
    soa_frame = soa_ms / 1000 * REF_RATE
    soa_dva = soa_ms / 1000 * line_vel
    motion_dur_frames = soa_frame + postFlashMotion_frame
    motion_dir = np.random.choice([-1, 1])
    xshift_steps = line_vel / REF_RATE * frame_repeat
    probe_xoffset = np.random.choice(probe_xoffset_base)
    line_start_xpos = probe_xoffset - (line_vel * probe2bar_ms / 1000) - \
                      (line_vel * soa_ms / 1000)

    # --------------------------------
    print('---------------------------')
    print(f'trial number    : {itrial + 1}')
    print(f'motion direction: {motion_dir}')

    # --------------------------------
    # /// create motion trajectory array
    line_end_xpos = (motion_dur_frames / frame_repeat * xshift_steps) + \
                    line_start_xpos

    motionX_array = np.linspace(line_start_xpos,
                                line_end_xpos,
                                num=int(motion_dur_frames/frame_repeat))
    motionX_array = motionX_array * motion_dir

    motionY_array = np.linspace(line_start_ypos,
                                line_end_ypos,
                                num=int(motion_dur_frames/frame_repeat))

    motionX_array = np.repeat(motionX_array, frame_repeat)
    motionY_array = np.repeat(motionY_array, frame_repeat)

    # /// update probe position according to motion direction
    probe.pos = [probe_xoffset * motion_dir, probe_yoffset]

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
    # for ifix in range(postFixGap):
    #     win.flip()

    # my_clock.reset()
    # motion_dur = npos * frame_repeat

    # move the vertical bar & flash the probe
    my_clock.reset()
    for i, icount in enumerate(range(len(motionX_array))):
        for islow in range(slow_coeff):
            vline.pos = (motionX_array[i], motionY_array[i])
            vline.draw()
            # fixdot1.draw()
            # fixdot2.draw()

            # flash the probe
            if icount == soa_frame:
                probe.draw()

            win.flip()

    motion_dur_measured = my_clock.getTime()
    # motion_dur_measured = round(my_clock.getTime(), 2)
    print(f'Motion duration: {motion_dur_measured} s')
    # print(f'Motion_dur_frames: {motion_dur_frames} frames')
    print(f'motion array length: {len(motionX_array)} frames')
    print(f'SOA: {soa_frame} frames')
    print(f'postFlashMotion: {postFlashMotion_frame} frames')
    print(f'Motion length: {abs(motionX_array[-1] - motionX_array[0])} dva')
    print(f'Motion velocity:'
          f'{abs(motionX_array[-1] - motionX_array[0]) / motion_dur_measured} '
          f'dva/s')
    print(f'line start: {motionX_array[0]} dva')
    print(f'line end: {motionX_array[-1]} dva')
    print(f'probe_x: {probe_xoffset}')


    click_pos = np.round(get_mouseclick(win), 2)
    # click_err = np.round(click_pos - probe.pos, 2)
    # print(f'probe position  : {probe.pos} dva')
    # print(f'click position  : {click_pos} dva')
    # print(f'click error     : {click_err} dva')

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
