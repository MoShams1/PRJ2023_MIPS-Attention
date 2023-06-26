"""
Mo Shams <MShamsCBR@gmail.com>
June 2023
---

The subject task is to localize a flashing probe in the presence of a moving
annulus.

15 repetitions
2 direction condisions (first half of rotatioin is considered): cw or ccw
2 annulus conditions: with and without visual marker
2 reversal conditions: with and without reversal

"""

import os
import random
import numpy as np
import pandas as pd
from psychopy import visual
from lib import config_visual as cvis, genpath, keymouse, timestamp
import warnings

# ----------------------------------------------------------------------------
# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = 'test'
rep_per_cnd = 15  # repetition per condition
full_screen = False

n_trials = rep_per_cnd * 2 * 2 * 2
frame_rate = 60
frame_repeat = 2  # flash duration [frames]
command_keys = {'quit_key': 'escape', 'response_key': 'space'}
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_folder = os.path.join('', '..', 'data')
image_folder = os.path.join('', '..', 'stimulus', 'image')

save_path = \
    os.path.join(save_folder,
                 f"{subID}_{timestamp.getdate()}_{timestamp.gettime()}.json")
# ----------------------------------------------------------------------------

# /// CONFIGURE VISUAL OBJECTS ///

# /// frame rate downsampling
# division by 60 to obtain 60 Hz (16.67 ms per frame) regardless of actual
# frame rate
frame_rate_rep = int(frame_rate / 60)
practical_fr = int(frame_rate / frame_rate_rep)

# /// background
bg_color = [0, 0, 0]

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
mov_size = 10
mov_dur = int(2 * practical_fr)  # in frames
# create orientation array (row 1: w/o rev | row 2: w/ rev)
rot_array_base = np.linspace(-90, 90, int(mov_dur / 2) + 1)
rot_array_rev = \
    np.concatenate((rot_array_base[:int(len(rot_array_base) / 2) + 1],
                    np.flip(rot_array_base[:int(len(rot_array_base) / 2)])))
rot_array = np.vstack((rot_array_base, rot_array_rev))

# /// flashing object(s)
probe_rad = .5  # radius of the probe
probe_color = 'red'
probe_pos = [0, 4]
probe_ori = rot_array[0, int(rot_array.shape[1] / 2)]

# ----------------------------------------------------------------------------

# # /// CONFIGURE MONITOR AND SCREEN ///

mon = cvis.configmon_dell()
win = cvis.configwin(mon=mon, screen=0,
                     fullscr=full_screen,
                     color=bg_color)
cvis.test_framerate(win=win, nominal_fr=frame_rate)
# ----------------------------------------------------------------------------

# /// CONDITIONING ///

ind_cnd = np.arange(n_trials)
np.random.shuffle(ind_cnd)

# annulus condition
ring_array = np.repeat(['marked', 'noise'], n_trials / 2)
ring_array = ring_array[ind_cnd]

# reversal condition
rev_array = np.tile(np.repeat([0, 1], n_trials / 2 / 2), 2)
rev_array = rev_array[ind_cnd]

# rotation direction condition
dir_array = np.tile(np.repeat(['cw', 'ccw'], n_trials / 2 / 2 / 2), 4)
dir_array = dir_array[ind_cnd]
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(1):

    # set image properties and load
    ring_directory = os.path.join(image_folder,
                                  f"ring_{ring_array[itrial]}.png")
    # load image
    ring = visual.ImageStim(win,
                            image=ring_directory,
                            size=mov_size,
                            opacity=.5,
                            pos=(0, 0))
    # adjust rotation direction
    if dir_array[itrial] == 'ccw':
        rot_array_tr = -rot_array
    else:
        rot_array_tr = rot_array

    # -------------------------------
    #
    #     # /// set up trial variables
    #
    #     # decide on starting point and rotating direction of the bar
    #     movobj_dir = 'cw'  # 'cw' or 'ccw'
    #     # movobj_theta_first = random.choice(range(180, 360, 10))
    #     movobj_theta_first = 270
    #     movobj_thetas = genpath.angular(theta1=movobj_theta_first,
    #                                     dur=movobj_dur,
    #                                     rotdir=movobj_dir)
    #     # decide on the frame number to show the flash
    #     probe_frame = probe_frame_list[itrial]
    #
    #     # decide on gap durations
    #     firstgap_dur = np.random.choice(gap_dur_arr)
    #     lastgap_dur = np.random.choice(gap_dur_arr)
    #     # -------------------------------
    #
    #     # /// run task
    #
    # # fixation period
    # for frame in range(fixdot_dur):
    #     cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
    #                    color=fixdot_color)
    #     win.flip()
    #
    # # gap period
    # for frame in range(firstgap_dur):
    #     win.flip()

    # motion period
    for iori in rot_array_tr[rev_array[itrial], :]:
        for irep in range(frame_repeat):
            ring.ori = iori
            ring.draw()
            if iori == probe_ori:
                cvis.addprobe(win=win, radius=probe_rad,
                              color=probe_color,
                              pos=probe_pos)
            win.flip()

#     # response period
#     click_loc = keymouse.get_mouseclick11(win)
#     # gap period
#     for frame in range(lastgap_dur):
#         win.flip()
#
#     # -------------------------------
#
#     # /// save data
#
#     # create a dictionary
#     trial_dict = {'trial_num': [itrial + 1],
#                   'probe_loc': [probe_pos_trial],
#                   'click_loc': [click_loc],
#                   'movobj_atflash': [movobj_atflash],
#                   'movobj_dur_sec': [movobj_dur_sec],
#                   'movobj_theta_first': [movobj_theta_first],
#                   'movobj_dir': [movobj_dir]}
#
#     # convert to data frame
#     dfnew = pd.DataFrame(trial_dict)
#
#     # if first trial create a file, else load and add the new data frame
#     if itrial == 0:
#         dfnew.to_json(save_path)
#     else:
#         df = pd.read_json(save_path)
#         dfnew = pd.concat([df, dfnew], ignore_index=True)
#         dfnew.to_json(save_path)
#
# win.close()
