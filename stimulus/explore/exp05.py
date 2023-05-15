"""
***** Project MIPS-SProf
***** Experiment 05

        Mo Shams <MShamsCBR@gmail.com>
        Initiated on: Jan 18, 2023

How does an unpredictable change in the moving object's trajectory
affect the mislocalization of a flashed probe in its vicinity?
"""

import os
import random
import numpy as np
import pandas as pd
from lib import config_visual as cvis, genpath, keymouse, timestamp

# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = 'MS1'
NTESTS = 5  # this indicates how often each probe position has to be tested
screen_num = 0  # 0: primary    1: secondary
frame_rate = 120
full_screen = True
condition_order = 'random'  # random / blocked

iblock = 0
command_keys = {'quit_key': 'escape', 'response_key': 'space'}
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_dir = os.path.join('../..', 'data', 'exp05', 'raw')
file_name = f"{subID}_{timestamp.getdate()}_{timestamp.gettime()}_" \
            f"{condition_order}.json"
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
fixdot_pos = [0, -5]
fixdot_color = 'white'
fixdot_dur = 1 * practical_fr  # sec x Hz = frames

# /// moving object
movobj_size = 5
movobj_thickness = 0.2
movobj_color = 'white'
movobj_pathlen = 11  # must be an odd number
movobj_dur = int(0.5 * practical_fr)  # sec x Hz = frames
movobj_atflash = None

# /// flashing object(s)
probe_rad = .4  # radius of the probe
probe_color = 'red'
probe_edge_offset = 0.5
PROBE_POSX = np.array([movobj_size / 2 + probe_edge_offset, 0])  # predefined
# position of the porbe

movobj_predir_arr = np.repeat([1, -1, 1, -1], NTESTS * 2)
movobj_postdir_arr = np.repeat([1, 1, -1, -1], NTESTS * 2)
probe_pos_temp1 = np.repeat([1, -1], NTESTS)
probe_pos_temp2 = np.repeat([1, -1], NTESTS)
probe_pos_temp3 = np.repeat([1, -1], NTESTS)
probe_pos_temp4 = np.repeat([1, -1], NTESTS)
np.random.shuffle(probe_pos_temp1)
np.random.shuffle(probe_pos_temp2)
np.random.shuffle(probe_pos_temp3)
np.random.shuffle(probe_pos_temp4)
probe_pos_arr = np.concatenate((probe_pos_temp1, probe_pos_temp2,
                                probe_pos_temp3, probe_pos_temp4))
cnd_arr = np.vstack((movobj_predir_arr,
                     movobj_postdir_arr,
                     probe_pos_arr)).transpose()
if condition_order == 'random':
    np.random.shuffle(cnd_arr)
ntrials = movobj_postdir_arr.shape[0]

# ----------------------------------------------------------------------------

# /// CONFIGURE MONITOR ///

mon = cvis.configmon_imac()
win = cvis.configwin(mon=mon, screen=screen_num,
                     fullscr=full_screen,
                     color=bg_color)
cvis.test_framerate(win=win, nominal_fr=frame_rate)
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(ntrials):

    # -------------------------------

    # /// set up trial variables

    # decide on gap durations
    firstgap_dur = np.random.choice(gap_dur_arr)
    lastgap_dur = np.random.choice(gap_dur_arr)

    # decide on the motion direction and adjust motion path and flash position
    movobj_pre_dir = random.choice([-1, 1])

    movobj_pathx, movobj_pathy = genpath.two_ways(pathlen=movobj_pathlen,
                                                  dur=movobj_dur,
                                                  cnd=cnd_arr[itrial])
    probe_posx_tr = cnd_arr[itrial][2] * PROBE_POSX
    probe_pos_tr = cnd_arr[itrial][0] * probe_posx_tr

    # -------------------------------

    # /// run task

    # information screen
    if itrial == 0:
        cvis.infoscreen_exp5(win, cmd=command_keys)

    if itrial % (NTESTS * 2) == 0:
        iblock += 1
        cvis.run_pause_screen(win=win, current_block=iblock,
                              cmd=command_keys, cnd=cnd_arr[itrial],
                              cnd_order=condition_order)

    # fixation period
    for frame in range(fixdot_dur):
        cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                       color=fixdot_color)
        win.flip()

    # gap period
    for frame in range(firstgap_dur):
        win.flip()

    # motion period
    for iframe in range(len(movobj_pathx)):
        for ifrrep in range(frame_rate_rep):
            cvis.addsquare(win=win, width=movobj_size, color=movobj_color,
                           fillcolor=bg_color,
                           pos=(movobj_pathx[iframe],
                                movobj_pathy[iframe]),
                           line_width=movobj_thickness)
            if movobj_pathx[iframe] == 0:
                cvis.addprobe(win=win, radius=probe_rad, color=probe_color,
                              pos=probe_pos_tr)
                # +++ TEST +++
                # cvis.showgrid(win, grid_n, grid_x_tr, grid_y_tr)
                # +++++++++++
            win.flip()

    # response period
    click_loc = keymouse.get_mouseclick_exp5(win, pos=fixdot_pos)

    # gap period
    for frame in range(lastgap_dur):
        win.flip()

    # -------------------------------

    # /// save data

    # create a dictionary
    trial_dict = {'trial_num': [itrial + 1],
                  'probe_loc': [probe_pos_tr],
                  'click_loc': [click_loc],
                  'movobj_flashpos': [[0, 0]],
                  'movobj_size': [movobj_size],
                  'movobj_dur': [round(movobj_dur / practical_fr, 2)],
                  'movobj_firstpos': [[movobj_pathx[0], movobj_pathy[0]]],
                  'movobj_lastpos': [[movobj_pathx[-1], movobj_pathy[-1]]],
                  'gap_dur': [round(firstgap_dur / practical_fr, 2)],
                  'cnd': [cnd_arr[itrial]]}

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
