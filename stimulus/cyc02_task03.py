"""
Mo Shams <MShamsCBR@gmail.com>
July 2023
---

The subject's task is to localize a flashing probe in the presence of a moving
annulus.

10 repetitions


"""

import os
import numpy as np
import pandas as pd
from psychopy import visual, core
from lib import config_visual as cvis, keymouse, timestamp
import warnings


def deg2rad(angle):
    return angle / 360 * 2 * np.pi


def pol2cart(rho, phi):
    phi = -phi + 90  # convert Psychopy deg to standard deg
    phi = deg2rad(phi)
    x_cart = rho * np.cos(phi)
    y_cart = rho * np.sin(phi)
    return x_cart, y_cart


# ----------------------------------------------------------------------------
# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = 'test'
rep_per_cnd = 10  # repetition per condition
full_screen = True
running_device = 'linux'  # 'linux' or 'mac'

n_trials = rep_per_cnd * 5 * 5
frame_rate = 60
frame_repeat = 2  # flash duration [frames]
command_keys = {'quit_key': 'escape', 'response_key': 'space'}
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_folder = os.path.join('', '..', 'data', 'cyc02')
image_folder = os.path.join('', '..', 'stimulus', 'image')

save_path = \
    os.path.join(save_folder,
                 f"{subID}_task03_{timestamp.getdate()}_"
                 f"{timestamp.gettime()}.json")
# ----------------------------------------------------------------------------

# /// CONFIGURE VISUAL OBJECTS ///

# /// frame rate downsampling
practical_fr = frame_rate

# /// background
bg_color = [0, 0, 0]

# /// temporal gap
# sec x Hz = frames
gap_dur_arr = np.round(np.arange(1, 1.5, .1) * practical_fr)
gap_dur_arr = gap_dur_arr.astype(int)

# /// fixation dot
fixdot_size = .7
fixdot_pos = (0, 0)
fixdot_color = 'black'
fixdot_dur = 1 * practical_fr  # sec x Hz = frames

# /// moving object
mov_size = 10
mov_dur_sec = 2  # sec per revolution
mov_dur = mov_dur_sec * int(practical_fr / frame_repeat)  # dur in frames
# create orientation array (row 1: w/o rev | row 2: w/ rev)
rot_array_org = np.linspace(-90, 0, int(mov_dur / 4))

# /// probe
probe_rad = .5  # radius of the probe
probe_color = 'red'
probe_ecc = 4  # probe eccentricity in dva
flash_at_ori = 0  # flash probe at annulus orientation/phase

# ----------------------------------------------------------------------------

# # /// CONFIGURE MONITOR AND SCREEN ///

if running_device == 'linux':
    mon = cvis.configmon_dell()
    win = cvis.configwin(mon=mon, fullscr=full_screen, color=bg_color)
else:
    mon = cvis.configmon_macair()
    win = cvis.configwin_macair(mon=mon, fullscr=full_screen, color=bg_color)
cvis.test_framerate(win=win, nominal_fr=frame_rate)
# ----------------------------------------------------------------------------

# /// CONDITIONING ///

ind_cnd = np.arange(n_trials)
np.random.shuffle(ind_cnd)

# probe to marker conditions
probe2mark_arr_sec = [-.3, -.15, 0, .15, .3]
probe2mark_arr_sec = np.repeat(probe2mark_arr_sec,
                               n_trials / len(probe2mark_arr_sec))
probe2mark_arr_sec = probe2mark_arr_sec[ind_cnd]

# probe to reversal conditions
probe2rev_arr_ind = np.linspace(-len(rot_array_org) + 1, 0, 5, dtype=int) - 1
probe2rev_arr_ind = np.tile(probe2rev_arr_ind,
                            int(n_trials / len(probe2rev_arr_ind)))
probe2rev_arr_ind = probe2rev_arr_ind[ind_cnd]

timer = core.Clock()
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(n_trials):

    if itrial == 2:
        cvis.run_pause_screen2(win)
    
    rot_offset = rot_array_org[probe2rev_arr_ind[itrial]]
    rot_array_tow = rot_array_org - rot_offset
    rot_array = np.concatenate((rot_array_tow[:-1], np.flip(rot_array_tow)))
    if 0 not in rot_array:
        print(f'rot_array: {rot_array}')
        raise ValueError("'rot_array' must contain the value '0'.")
    
    # -------------------------------

    # /// set up trial variables

    # decide on annulus type
    ring_directory = os.path.join(image_folder, "ring_marked.png")
    ring = visual.ImageStim(win,
                            image=ring_directory,
                            size=mov_size, pos=(0, 0))

    rot_array_tr = rot_array
    
    probe2rev_deg = -rot_offset
    probe2rev_sec = probe2rev_deg * mov_dur_sec / 360

    # decide on position wrt to the marker
    probe2mark_sec = probe2mark_arr_sec[itrial]
    probe2mark_deg = probe2mark_sec * 360 / mov_dur_sec
    probe_loc = pol2cart(probe_ecc, probe2mark_deg)

    # decide on gap durations
    firstgap_dur = np.random.choice(gap_dur_arr)
    lastgap_dur = np.random.choice(gap_dur_arr)

    print('\t-----------------------')
    print(f'\n\tflash2rev = {probe2rev_sec} sec')
    print(f'\tflash2mark = {probe2mark_sec} sec')
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
    timer.reset()
    for ind_ori, iori in enumerate(rot_array_tr):
        for irep in range(frame_repeat):
            ring.ori = iori
            ring.draw()
            if (iori == flash_at_ori) and \
                    (ind_ori >= (len(rot_array) / 2) - 1):
                cvis.addprobe(win=win, radius=probe_rad,
                              color=probe_color,
                              pos=probe_loc)
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
                  'frame_rate': [frame_rate],
                  'frame_repeat': [frame_repeat],
                  'probe2mark_ms': [np.round(probe2mark_sec*1000)],
                  'probe2mark_deg': [probe2mark_deg],
                  'probe2rev_ms': [np.round(probe2rev_sec*1000)],
                  'probe2rev_deg': [probe2rev_deg],
                  'probe_loc': [probe_loc],
                  'click_loc': [click_loc]}

    # convert to data frame
    dfnew = pd.DataFrame(trial_dict)

    # if first trial create a file, else load and add the new data frame
    if itrial == 0:
        dfnew.to_json(save_path)
    else:
        df = pd.read_json(save_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
        dfnew.to_json(save_path)

win.close()
