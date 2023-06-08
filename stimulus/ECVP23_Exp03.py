"""
Project MIPS-SProf
Mo Shams <MShamsCBR@gmail.com>
Initiated on: Feb 27, 2023
---

TEMPORAL PROFILE OF THE ANISOTROPY (ECVP23 - Experiment 03)
    predictable moving object's trajectory
    predictable location of the bar at the time of flash

TASK OVERVIEW
- A bar rotates around the gaze.
- After the bar disappears, the flash has to be localized.

"""

import os
import random
import numpy as np
import pandas as pd
from lib import config_visual as cvis, genpath, keymouse, timestamp
import warnings
# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = '0013'
n_tests_per_position = 5
screen_num = 0  # 0: primary    1: secondary
frame_rate = 60
full_screen = True

command_keys = {'quit_key': 'escape', 'response_key': 'space'}
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_dir = os.path.join('', '..', 'data', 'ECVP23_Exp03')
file_name = f"{subID}_{timestamp.getdate()}_{timestamp.gettime()}.json"
save_address = os.path.join(save_dir, file_name)
# ----------------------------------------------------------------------------

# /// CONFIGURE VISUAL OBJECTS ///

# /// frame rate downsampling
# division by 60 to obtain 60 Hz (16.67 ms per frame) regardless of actual
# frame rate
frame_rate_rep = int(frame_rate / 60)
practical_fr = int(frame_rate / frame_rate_rep)

# /// background
bg_color = 'black'

# /// temporal gap
# sec x Hz = frames
gap_dur_arr = np.round(np.arange(1, 1.5, .1) * practical_fr)
gap_dur_arr = gap_dur_arr.astype(int)

# /// fixation dot
fixdot_size = .7
fixdot_pos = (0, 0)
fixdot_color = 'white'
fixdot_dur = 1 * practical_fr  # sec x Hz = frames

# /// moving object
movobj_size = [.3, 3]
movobj_color = 'white'
movobj_path_radius = 5
movobj_dur_sec = 1
movobj_dur = int(movobj_dur_sec * practical_fr) - 1  # sec x Hz = frames
# make sure movobj_dur is a factor of 3 and an odd number
assert movobj_dur % 2 == 1, 'Number of frames is not an odd number.'

movobj_atflash = None

# /// flashing object(s)
probe_rad = .5  # radius of the probe
probe_color = 'red'
probe_quarter_frame = int(movobj_dur / 4)
probe_frame_list = list(range(15, 43 + 1, 2))
ntrials = n_tests_per_position * len(probe_frame_list)
probe_frame_list = np.array(probe_frame_list)
probe_frame_list = np.repeat(probe_frame_list, n_tests_per_position)
np.random.shuffle(probe_frame_list)
probe_frame_offset_coeff = 4  # tolerance to deviate from midway
probe_frame_limit = int(movobj_dur / probe_frame_offset_coeff)
# generate test grid
probe_pos_trial = [0, 5]

# turn of Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# ----------------------------------------------------------------------------

# /// CONFIGURE MONITOR ///

mon = cvis.configmon_dell()
win = cvis.configwin(mon=mon, screen=screen_num,
                     fullscr=full_screen,
                     color=bg_color)
cvis.test_framerate(win=win, nominal_fr=frame_rate)
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(ntrials):

    # -------------------------------

    # /// set up trial variables

    # decide on starting point and rotating direction of the bar
    movobj_dir = 'cw'  # 'cw' or 'ccw'
    # movobj_theta_first = random.choice(range(180, 360, 10))
    movobj_theta_first = 270
    movobj_thetas = genpath.angular(theta1=movobj_theta_first,
                                    dur=movobj_dur,
                                    rotdir=movobj_dir)
    # decide on the frame number to show the flash
    probe_frame = probe_frame_list[itrial]

    # decide on gap durations
    firstgap_dur = np.random.choice(gap_dur_arr)
    lastgap_dur = np.random.choice(gap_dur_arr)
    # -------------------------------

    # /// run task

    # fixation period
    for frame in range(fixdot_dur):
        cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                       color=fixdot_color)
        win.flip()

    # gap period
    for frame in range(firstgap_dur):
        win.flip()

    # motion period
    for iframe in range(movobj_dur):
        for ifrrep in range(frame_rate_rep):
            cvis.addbar(win=win, size=movobj_size, color=movobj_color,
                        theta=movobj_thetas[iframe], radius=movobj_path_radius)
            if iframe == probe_frame:
                cvis.addprobe2(win=win, radius=probe_rad,
                               color=probe_color,
                               pos=probe_pos_trial)
                # %%% TEST %%%
                # for itest in range(60):
                #     cvis.addbar(win=win, size=movobj_size, color=movobj_color,
                #                 theta=movobj_thetas[iframe],
                #                 radius=movobj_path_radius)
                #     cvis.addprobe2(win=win, radius=probe_rad,
                #                    color=probe_color,
                #                    pos=probe_pos_trial)
                #     win.flip()
                # -------------

                movobj_atflash = movobj_thetas[iframe]
            win.flip()

    # response period
    click_loc = keymouse.get_mouseclick11(win)
    # gap period
    for frame in range(lastgap_dur):
        win.flip()

    # -------------------------------

    # /// save data

    # create a dictionary
    trial_dict = {'trial_num': [itrial + 1],
                  'probe_loc': [probe_pos_trial],
                  'click_loc': [click_loc],
                  'movobj_atflash': [movobj_atflash],
                  'movobj_dur_sec': [movobj_dur_sec],
                  'movobj_theta_first': [movobj_theta_first],
                  'movobj_dir': [movobj_dir]}

    # convert to data frame
    dfnew = pd.DataFrame(trial_dict)

    # if first trial create a file, else load and add the new data frame
    if itrial == 0:
        dfnew.to_json(save_address)
    else:
        df = pd.read_json(save_address)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
        dfnew.to_json(save_address)

win.close()
