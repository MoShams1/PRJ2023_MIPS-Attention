"""
***** project: PRJ2023_MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Oct 2024

Task Procedure:
    A vertical bar moves horizontally 10 dva/s along a path of 10 (-5 dva to +5 dva with a random offset of ±1 dva
    A probe flashes at -4 dva to +4 dva from the bar, at the time the bar
    reaches the midway of its path.

"""

import os
import random
import warnings
import numpy as np
import pandas as pd
from lib import stim_flow_control as sfc
from psychopy import event, visual, core


def get_mouseclick(win, mouse_correctionFactor=1):
    ms_posx = random.choice(np.arange(-2, 2 + .1, .1))
    ms_posy = -2
    mouse = event.Mouse(win=win, visible=True,
                        newPos=[ms_posx * mouse_correctionFactor,
                                ms_posy * mouse_correctionFactor])
    while not mouse.getPressed()[0]:
        escape_session()  # force exit with 'escape' button
        win.flip()
    while mouse.getPressed()[0]:
        pass
    click_loc = mouse.getPos() / mouse_correctionFactor
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

subID = '0001'  # subject ID (put 'test' for a test run)
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

output_name = f"cyc05_exp01_{date}_{time}_{subID}.json"

# set data directory
save_path = os.path.join("..", "data", "cyc05", output_name)

# --------------------------------
# /// set stimulus parameters

# initialize the display and the keyboard
refresh_rate = 60

# define the flash duration in frames
frame_repeat = 2

# configure the monitor and the stimulus window
bg_color = [-.8, -.8, -.8]
mon = sfc.config_mon_dell()
win = sfc.config_win(mon=mon, fullscr=full_screen, color=bg_color)
sfc.test_refresh_rate(win, refresh_rate)

# fixation mark
fixdot_radius = .2
fixMark_x = 0
fixMark_y = -2
fixdot_color = 'white'

# probe
probe_rad = .3
probe_color = 'red'
probe2bar_base_dva = np.arange(-4, 4 + .1, .5)
probe_y = 4

# lines
bar_width = 0.1
bar_length = 2
bar_color = 'white'
bar_vel = 10  # dva/s
bar_ystart = 4  # dva
bar_yend = 4  # dva
motion_dur_ms = 1000
motion_dur_frames = int(motion_dur_ms / 1000 * refresh_rate)
motion_dir_base = np.array([-1, 1])

# potential gap durations (0.75 - 1.25 sec)
gap_durations_base = range(int(refresh_rate * .75),
                           int(refresh_rate * 1.25) + 1, 1)

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

ncnds = 17 * 2
# probe2bar x motionDirection

probe2bar_array_dva = np.repeat(probe2bar_base_dva, 2)
motion_dir_array = np.tile(motion_dir_base, 17)

rep_per_cnd = 5
probe2bar_array_dva = np.repeat(probe2bar_array_dva, rep_per_cnd)
motion_dir_array = np.repeat(motion_dir_array, rep_per_cnd)

ntrials = ncnds * rep_per_cnd
ind_shuffle = np.arange(ntrials)
np.random.shuffle(ind_shuffle)
probe2bar_array_dva = probe2bar_array_dva[ind_shuffle]
motion_dir_array = motion_dir_array[ind_shuffle]

assert (probe2bar_array_dva.size == ntrials)
assert (motion_dir_array.size == ntrials)

# ----------------------------------------------------------------------------
# /// CREATE VISUAL OBJECTS ///

# bar
bar = visual.Rect(win=win,
                  size=(bar_width, bar_length),
                  fillColor=bar_color)

# probe
probe = visual.Circle(win,
                      radius=probe_rad,
                      fillColor=probe_color)

# fixation dot
fixdot1 = visual.Circle(win,
                        radius=fixdot_radius,
                        pos=(fixMark_x, fixMark_y),
                        fillColor=fixdot_color)
fixdot2 = visual.Circle(win,
                        radius=fixdot_radius * .7,
                        pos=(fixMark_x, fixMark_y),
                        fillColor=bg_color)

# ----------------------------------------------------------------------------
# /// OTHER SETTINGS ///

# pause trials
nblocks = rep_per_cnd  # number of blocks
pause_array = np.linspace(0, ntrials, nblocks + 1)
pause_array = pause_array[:-1]

# initialize mouse
mouse = event.Mouse(win=win, visible=False)

# initialize clock
my_clock = core.Clock()

# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

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
    probe2bar_dva = probe2bar_array_dva[itrial]
    motion_dir = motion_dir_array[itrial]

    bar_xoffset = random.choice(np.arange(-1, 1.1, .1))
    bar_xstart = -5 + bar_xoffset
    bar_xend = 5 + bar_xoffset
    probe_x = probe2bar_dva + bar_xoffset

    # --------------------------------
    # /// create motion trajectory array
    bar_xarray = np.linspace(bar_xstart,
                             bar_xend,
                             num=int(motion_dur_frames / frame_repeat))

    bar_yarray = np.linspace(bar_ystart,
                             bar_yend,
                             num=int(motion_dur_frames / frame_repeat))

    bar_xarray = np.repeat(bar_xarray, frame_repeat)
    bar_yarray = np.repeat(bar_yarray, frame_repeat)

    # /// update probe and bar horizontal locations according to motion dir
    bar_xarray = bar_xarray * motion_dir
    probe.pos = [probe_x * motion_dir, probe_y]

    # --------------------------------
    # /// run stimulus

    # show the block screeen
    if itrial in pause_array:
        sfc.block_msg3(win, np.where(pause_array == itrial)[0][0] + 1,
                       nblocks, color='white')

    # inter-trial interval gap period
    for igap in range(iti):
        win.flip()

    # fixation period
    for ifix in range(refresh_rate):
        fixdot1.draw()
        fixdot2.draw()
        win.flip()
        escape_session()

    # post-fixation gap period
    for ifix in range(postFixGap):
        win.flip()

    # move the vertical bar & flash the probe
    my_clock.reset()
    probe_time = np.nan
    motion_dur_frames = len(bar_xarray)
    halfway_frame = motion_dur_frames / 2
    motion_start_time = my_clock.getTime() * 1000

    for i in range(motion_dur_frames):
        for islow in range(slow_coeff):
            bar.pos = (bar_xarray[i], bar_yarray[i])
            bar.draw()

            # flash the probe
            if (i == halfway_frame) | (i == halfway_frame + 1):
                probe_time = my_clock.getTime() * 1000
                probe.draw()

            win.flip()

    motion_end_ms = my_clock.getTime() * 1000

    print('---------------------------')
    print(f'trial number    : {itrial + 1}')
    print(f'motion direction: {motion_dir}')
    motion_dur_measured_ms = motion_end_ms - motion_start_time
    probe2bar_measured_ms = probe_time - motion_start_time
    flash2motionEnd_measured_ms = motion_end_ms - probe_time
    print(f'probe2bar_dva: {probe2bar_dva} dva')
    print(f'bar_xoffset: {bar_xoffset * motion_dir}')
    print(f'bar_xstart: {bar_xarray[0]}')
    print(f'bar_xend: {bar_xarray[-1]}')
    print(f'probe_x  : {round(probe.pos[0], 2)} dva')
    print(f'Motion duration measured: {round(motion_dur_measured_ms)} ms')
    motion_distance = abs(bar_xarray[-1] - bar_xarray[0])
    motion_vel_measured = abs(motion_distance) / motion_dur_measured_ms * 1000
    print(f'Motion velocity: {round(motion_vel_measured, 2)} dva/s')

    click_pos = np.round(get_mouseclick(win), 2)
    click_err = np.round(click_pos - probe.pos, 2)
    print(f'click position  : {click_pos} dva')
    print(f'click error     : {click_err} dva')

    # --------------------------------
    # /// save trial parameters

    trial_dict = {'trial_num': itrial + 1,
                  'probe2bar_dva': probe2bar_dva,
                  'probe_pos': [probe.pos],
                  'flash2barEnd_measured_ms': flash2motionEnd_measured_ms,
                  'motion_dir': motion_dir,
                  'motion_duration_ms_measure': motion_dur_measured_ms,
                  'motion_vel_measured': motion_vel_measured,
                  'bar_xoffset': bar_xoffset * motion_dir,
                  'bar_xstart': bar_xarray[0],
                  'bar_xend': bar_xarray[-1],
                  'bar_ystart': bar_ystart,
                  'bar_yend': bar_yend,
                  'click_pos': [click_pos],
                  'click_xerr': click_err[0],
                  'click_yerr': click_err[1]}

    dfnew = pd.DataFrame(trial_dict)
    # if not first trial, load the existing data frame and concatenate
    if itrial > 0:
        df = pd.read_json(save_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
    dfnew.to_json(save_path)

    if itrial == ntrials - 1:
        sfc.end_screen(win, color='white')

# --------------------------------
win.close()
