"""
Mo Shams <MShamsCBR@gmail.com>
June 2023
---

The subject's task is to localize a flashing probe in the presence of a
rotating annulus.

9 repetitions
2 direction condisions (first half of rotatioin is considered): cw or ccw
3 annulus conditions: w/ close marker, w/ remote marker, w/o marker
2 reversal conditions: with and without reversal

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
rep_per_cnd = 9  # repetition per condition
full_screen = True
running_device = 'linux'  # 'linux' or 'mac'

n_trials = rep_per_cnd * 3 * 2 * 2
frame_rate = 60
frame_repeat = 2  # flash duration [frames]
command_keys = {'quit_key': 'escape', 'response_key': 'space'}
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_folder = os.path.join('', '..', 'data', 'cyc02')
image_folder = os.path.join('', '..', 'stimulus', 'image')

save_path = \
    os.path.join(save_folder,
                 f"{subID}_task01_{timestamp.getdate()}_"
                 f"{timestamp.gettime()}.json")
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
fixdot_color = 'black'
fixdot_dur = 1 * practical_fr  # sec x Hz = frames

# /// moving object
mov_size = 10
mov_dur = int(2 * practical_fr / frame_repeat)  # one revolution in frames
# create orientation array (row 1: w/o rev | row 2: w/ rev)
rot_array_base = np.linspace(-90, 90, int(mov_dur / 2) - 1)
rot_array_rev = \
    np.concatenate((rot_array_base[:int(len(rot_array_base) / 2) + 1],
                    np.flip(rot_array_base[:int(len(rot_array_base) / 2)])))
rot_array = np.vstack((rot_array_base, rot_array_rev))
# /// probe
probe_rad = .5  # radius of the probe
probe_color = 'red'

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

# annulus conditions
ring_array = np.repeat(['marked', 'marked_inv', 'noise'],
                       n_trials / 3)[ind_cnd]

# reversal conditions
rev_array = np.tile(np.repeat([0, 1], n_trials / 3 / 2), 3)[ind_cnd]

# rotation direction conditions
dir_array = np.tile(np.repeat(['cw', 'ccw'], n_trials / 3 / 2 / 2), 6)[ind_cnd]

# probe position conditions
offset_array_deg = [-10, 0, 10]
offset_array_deg = np.tile(
    np.repeat(offset_array_deg, n_trials / 3 / 2 / 2 / 3), 12)[ind_cnd]

timer = core.Clock()
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(n_trials):

    # -------------------------------

    # /// set up trial variables

    # decide on annulus type
    ring_directory = os.path.join(image_folder,
                                  f"ring_{ring_array[itrial]}.png")
    opacity = .5 if ring_array[itrial] == 'noise' else 1
    ring = visual.ImageStim(win,
                            image=ring_directory,
                            size=mov_size,
                            opacity=opacity,
                            pos=(0, 0))
    # decide on rotation direction and reversal
    if dir_array[itrial] == 'ccw':
        rot_array_tr = -rot_array[rev_array[itrial], :] \
                       + offset_array_deg[itrial]
    else:
        rot_array_tr = rot_array[rev_array[itrial], :] \
                       + offset_array_deg[itrial]

    # decide on flash time
    flash_at_ori = rot_array_tr[int(len(rot_array_tr) / 2)]

    # decide on flash position
    # convert annulus coordinate to triang. co.
    probe_ori = -offset_array_deg[itrial] + 90
    probe_pos = np.round(pol2cart(4, probe_ori), 2)

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
    timer.reset()
    for iori in rot_array_tr:
        for irep in range(frame_repeat):
            ring.ori = iori
            ring.draw()
            if iori == flash_at_ori:
                cvis.addprobe(win=win, radius=probe_rad,
                              color=probe_color,
                              pos=probe_pos)
            win.flip()
    delta_t = timer.getTime()
    print(delta_t*1000)
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
                  'probe_loc': [probe_pos],
                  'click_loc': [click_loc],
                  'mov_traj': [rot_array_tr],
                  'cnd_dir': [dir_array[itrial]],
                  'cnd_rev': [rev_array[itrial]],
                  'cnd_probe_pos': [offset_array_deg[itrial]],
                  'cnd_annulus': [ring_array[itrial]]}

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
