"""
Project MIPS-Anisotropy (Exploration 11)
Mo Shams <MShamsCBR@gmail.com>
Initiated on: Feb 20, 2023
---

SPATIAL PROFILE OF THE ANISOTROPY

- A bar rotates around the fixation dot.
- The path and the phase of the trajectory is constant.
- When the bar is at top, a probe flashes at different positions wrt the bar.
- The time of the flash is constant and predictable according to the bar's
trajectory.
- The position of the flash is not predictable.

"""

import os
import random
import numpy as np
import pandas as pd
from lib import config_visual as cvis, genpath, keymouse, timestamp

# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = 'test'
NTRIALS = 1
screen_num = 1  # 0: primary    1: secondary
frame_rate = 120
full_screen = False

command_keys = {'quit_key': 'escape', 'response_key': 'space'}
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_dir = os.path.join('../..', 'data', 'raw')
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
movobj_size = [.15, 3]
movobj_color = 'white'
movobj_path_radius = 5
movobj_theta_first = 270
movobj_theta_last = movobj_theta_first + 360
movobj_dur_sec = 2
movobj_dur = int(movobj_dur_sec * practical_fr)-1  # sec x Hz = frames
# make sure movobj_dur is a factor of 3 and an odd number
assert movobj_dur % 2 == 1, 'Number of frames is not an odd number.'

movobj_atflash = None
movobj_thetas = genpath.angular(theta1=movobj_theta_first,
                                theta2=movobj_theta_last,
                                dur=movobj_dur)

# /// test grid
# grid_width = 12
# grid_n = NGRIDS

# /// flashing object(s)
probe_rad = .4  # radius of the probe
probe_color = 'red'
probe_frame = int(movobj_dur / 2)  # frame num where the probe flashes

# generate probe positions
probe_xpos_list = np.arange(-2, 2, .5)
probe_ypos = 5
# ----------------------------------------------------------------------------

# /// CONFIGURE MONITOR ///

mon = cvis.configmon_imac()
win = cvis.configwin(mon=mon, screen=screen_num,
                     fullscr=full_screen,
                     color=bg_color)
# cvis.test_framerate(win=win, nominal_fr=frame_rate)
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(NTRIALS):
    # -------------------------------

    # /// set up trial variables

    # decide on gap durations
    firstgap_dur = np.random.choice(gap_dur_arr)
    lastgap_dur = np.random.choice(gap_dur_arr)

    # decide on the motion direction and adjust motion path and flash position
    probe_xpos_trial = random.choice(probe_xpos_list)
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
                               pos=(-2, probe_ypos))
            win.flip()

    # response period
    # click_loc = keymouse.get_mouseclick(win)

    # gap period
    for frame in range(lastgap_dur):
        win.flip()

    # -------------------------------
    #
    # # /// save data
    #
    # # create a dictionary
    # trial_dict = {'trial_num': [itrial + 1],
    #               'probe_loc': [probe_pos_tr],
    #               'click_loc': [click_loc],
    #               'movobj_flashpos': [movobj_atflash],
    #               'movobj_size': [movobj_size],
    #               'movobj_dur': [round(movobj_dur / practical_fr, 2)],
    #               'movobj_firstpos': [(movobj_pathx_tr[0],
    #                                    movobj_pathy_tr[0])],
    #               'movobj_lastpos': [(movobj_pathx_tr[-1],
    #                                   movobj_pathy_tr[-1])],
    #               'movobj_dir': movobj_dir,
    #               'gap_dur': [round(firstgap_dur / practical_fr, 2)]}
    #
    # # convert to data frame
    # dfnew = pd.DataFrame(trial_dict)
    #
    # # if first trial create a file, else load and add the new data frame
    # if itrial == 0:
    #     dfnew.to_json(save_address)
    # else:
    #     df = pd.read_json(save_address)
    #     dfnew = pd.concat([df, dfnew], ignore_index=True)
    #     dfnew.to_json(save_address)

win.close()
