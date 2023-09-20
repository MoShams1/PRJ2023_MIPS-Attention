"""
***** Project MIPS-Attention *****

    Mo Shams <MShamsCBR@gmail.com>
    Initiated: Feb 27, 2023
    Modified: Sep 20, 2023

Conditions:
    delta t: -250:100:250 ms

Prodedure
    A bar moves either rightward or leftward
    A dot flashes on at different time relative to bar's sweep
    After the bar disappears, subject has to localize the flashed object

"""

import os
import numpy as np
import pandas as pd
from lib import config_visual as cvis, genpath, keymouse, timestamp
from psychopy import visual
import warnings

# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = 'test'
n_times = 6
n_dirs = 2
n_rep_per_cnd = 6
n_trials = n_times * n_dirs * n_rep_per_cnd
screen_num = 0  # 0: primary    1: secondary
frame_rate = 60
full_screen = False

command_keys = {'quit_key': 'escape', 'response_key': 'space'}
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_dir = os.path.join('', '..', 'data', 'cyc02')
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
bg_color = [0, 0, 0]

# /// temporal gap
# sec x Hz = frames
gap_dur_arr = np.round(np.arange(1, 1.5, .1) * practical_fr)
gap_dur_arr = gap_dur_arr.astype(int)

# /// fixation dot
fixdot_size = .5
fixdot_color = 'black'
fixdot_dur = 1 * practical_fr  # sec x Hz = frames

# /// moving object
movobj_size = [.2, 3]
movobj_color = 'black'
movobj_dur_sec = 1
movobj_dur = int(movobj_dur_sec * practical_fr)  # sec x Hz = frames
movobj_first_pos = -7

movobj_atflash = None

# /// flashing object(s)
probe_rad = .3  # radius of the probe
probe_color = 'tomato'

# generate test grid
probe_pos_trial = [0, 3]
# ----------------------------------------------------------------------------

# /// CONDITIONING ///

ind_cnd = np.arange(n_trials)
np.random.shuffle(ind_cnd)

# probe time
probe_frame_list_ms = np.arange(-250, 250 + 1, 100)
probe_frame_list_ms = np.array(probe_frame_list_ms)
probe_frame_list_ms = np.tile(probe_frame_list_ms, int(n_trials / n_times))
probe_frame_list_ms = probe_frame_list_ms[ind_cnd]  # [in ms]
probe_frame_list = probe_frame_list_ms / 1000 * 60 + 30  # [in frames]

# motion direction
dir_arr_base = np.array([-1, 1])
dir_arr = np.repeat(dir_arr_base, int(n_trials / n_dirs))
dir_arr = dir_arr[ind_cnd]

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

for itrial in range(n_trials):

    # -------------------------------

    fixdot_pos = np.random.choice(np.arange(-.5, .5, .1), 1)[0], 0

    # /// set up trial variables

    movobj_dir = dir_arr[itrial]

    path_x, path_y = genpath.linear(pos1=[movobj_first_pos, 0],
                                    pos2=[-movobj_first_pos, 0],
                                    dur=movobj_dur)
    if dir_arr[itrial] == -1:
        path_x = np.flip(path_x)

    bar = visual.Rect(win,
                      size=movobj_size,
                      fillColor='black')

    # decide on the frame number to show the flash
    probe_frame = probe_frame_list[itrial]

    # decide on gap durations
    firstgap_dur = np.random.choice(gap_dur_arr)
    lastgap_dur = np.random.choice(gap_dur_arr)

    print('---------------------')
    print(f'trial: {itrial + 1}')
    print(f'direction: {dir_arr[itrial]}')
    print(f'flash2bar = {probe_frame_list_ms[itrial]} ms')

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
            bar.pos = path_x[iframe], 3
            bar.draw()
            if iframe == probe_frame:
                cvis.addprobe(win=win, radius=probe_rad,
                              color=probe_color,
                              pos=probe_pos_trial)
                # %%% TEST %%%
                # for itest in range(60):
                #     bar.draw()
                #     cvis.addprobe(win=win, radius=probe_rad,
                #                   color=probe_color,
                #                   pos=probe_pos_trial)
                #     win.flip()
                # -------------
                movobj_atflash = np.round(path_x[iframe], 2)
                if dir_arr[itrial] == -1:
                    movobj_atflash = -movobj_atflash
                print(f'flash2bar = {movobj_atflash} dva')
            win.flip()

    # response period
    click_loc = keymouse.get_mouseclick11(win)
    # gap period
    for frame in range(lastgap_dur):
        win.flip()

    # -------------------------------
    print(f'click_loc = {click_loc[0] - probe_pos_trial[0]}')

    # /// save data

    # create a dictionary
    trial_dict = {'trial_num': [itrial + 1],
                  'probe_loc': [probe_pos_trial],
                  'click_loc': [click_loc],
                  'flash2bar_time': [probe_frame_list_ms[itrial]],
                  'flash2bar_angle': [movobj_atflash],
                  'movobj_dur_sec': [movobj_dur_sec],
                  'movobj_first_pos': [movobj_first_pos],
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
