"""
***** Project MIPS-Anisotropy
***** Experiment 01

        Mo Shams <MShamsCBR@gmail.com>
        Initiated on: Jan 03, 2023

In this experiment, my aim is to map the mislocalization of single flashed
probe in the vicinity of a moving object in high resolution.
"""

import os
import random
import numpy as np
import pandas as pd
from lib import visual, genpath, keymouse, timestamp

# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = 'test'
NTESTS = 3  # this indicates how often each probe position has to be tested
NGRIDS = (2, 2)  # number of dots along each dimension (x, y)
NTRIALS = NTESTS * NGRIDS[0] * NGRIDS[1]
screen_num = 0  # 0: primary    1: secondary
frame_rate = 120
full_screen = True

iblock = 0
pause_after = 27
nblocks = int(NTRIALS / pause_after)
command_keys = {'quit_key': 'escape', 'response_key': 'space'}
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_dir = os.path.join('..', 'data', 'raw')
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
movobj_size = 5
movobj_color = 'white'
movobj_firstpos = (-5, 5)
movobj_lastpos = (5, 5)  # two potential last positions
movobj_dur = int(.5 * practical_fr)  # sec x Hz = frames
movobj_atflash = None
movobj_pathx, movobj_pathy = genpath.linear(pos1=movobj_firstpos,
                                            pos2=movobj_lastpos,
                                            dur=movobj_dur)

# /// test grid
grid_width = 12
grid_n = NGRIDS

# /// flashing object(s)
probe_rad = .4  # radius of the probe
probe_color = 'red'
probe_frame = int(movobj_dur / 2)  # frame number where the probe should flash

# generate test grid
grid_x, grid_y = visual.gengrid(width=grid_width, n=grid_n,
                                movpos1=movobj_firstpos,
                                movpos2=movobj_lastpos)

# generate probe positions
grid_x_arr = grid_x.flatten()
grid_y_arr = grid_y.flatten()
probe_pos_temp = list(zip(grid_x_arr, grid_y_arr))
probe_pos_list = []
for itest in range(NTESTS):
    probe_pos_list = probe_pos_list + probe_pos_temp
random.shuffle(probe_pos_list)
# ----------------------------------------------------------------------------

# /// CONFIGURE MONITOR ///

mon = visual.configmon_imac()
win = visual.configwin(mon=mon, screen=screen_num,
                       fullscr=full_screen,
                       color=bg_color)
visual.test_framerate(win=win, nominal_fr=frame_rate)
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(NTRIALS):
    # -------------------------------

    # /// set up trial variables

    # decide on gap durations
    firstgap_dur = np.random.choice(gap_dur_arr)
    lastgap_dur = np.random.choice(gap_dur_arr)

    # decide on the motion direction and adjust motion path and flash position
    movobj_dir = random.choice([-1, 1])
    if movobj_dir == -1:
        movobj_pathx_tr = -movobj_pathx
        probe_pos_tr = (-probe_pos_list[itrial][0],
                        probe_pos_list[itrial][1])
        grid_x_tr = -grid_x
    else:
        movobj_pathx_tr = movobj_pathx
        probe_pos_tr = (probe_pos_list[itrial][0],
                        probe_pos_list[itrial][1])
        grid_x_tr = grid_x
    movobj_pathy_tr = movobj_pathy
    grid_y_tr = grid_y
    # -------------------------------

    # /// run task

    # information screen
    if itrial % pause_after == 0:
        iblock += 1
        visual.infoscreen(win, iblock=iblock, nblocks=nblocks,
                          cmd=command_keys)

    # fixation period
    for frame in range(fixdot_dur):
        visual.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                         color=fixdot_color)
        win.flip()

    # gap period
    for frame in range(firstgap_dur):
        win.flip()

    # motion period
    for iframe in range(movobj_dur):
        for ifrrep in range(frame_rate_rep):
            visual.addsquare(win=win, width=movobj_size, color=movobj_color,
                             fillcolor=bg_color,
                             pos=(movobj_pathx_tr[iframe],
                                  movobj_pathy_tr[iframe]))
            if iframe == probe_frame:
                visual.addprobe(win=win, radius=probe_rad, color=probe_color,
                                pos=probe_pos_tr)
                movobj_atflash = (movobj_pathx_tr[iframe],
                                  movobj_pathy_tr[iframe])
                # +++ TEST +++
                # visual.showgrid(win, grid_n, grid_x_tr, grid_y_tr)
                # +++++++++++
            win.flip()

    # response period
    click_loc = keymouse.get_mouseclick(win)

    # gap period
    for frame in range(lastgap_dur):
        win.flip()

    # -------------------------------

    # /// save data

    # create a dictionary
    trial_dict = {'trial_num': [itrial + 1],
                  'probe_loc': [probe_pos_tr],
                  'click_loc': [click_loc],
                  'movobj_flashpos': [movobj_atflash],
                  'movobj_size': [movobj_size],
                  'movobj_dur': [round(movobj_dur / practical_fr, 2)],
                  'movobj_firstpos': [(movobj_pathx_tr[0],
                                       movobj_pathy_tr[0])],
                  'movobj_lastpos': [(movobj_pathx_tr[-1],
                                      movobj_pathy_tr[-1])],
                  'movobj_dir': movobj_dir,
                  'gap_dur': [round(firstgap_dur / practical_fr, 2)]}

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
