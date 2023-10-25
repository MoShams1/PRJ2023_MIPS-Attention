"""
***** project: MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Oct 2023


Task Procedure:

    In

There are two direction conditions:
    d =


"""

import os
import random
import warnings
import numpy as np
import pandas as pd
from lib import stim_flow_control as sfc
from psychopy import event, visual, core

# disable Panda's false warning message
pd.options.mode.chained_assignment = None  # default='warn'

# ----------------------------------------------------------------------------
# /// INSERT SESSION'S META DATA ///

subID = 'test'
nrep = 10
nstm = 2  # number of stimuli (FG, FG_edge, BB, WB, FE1, FE2)
ndir = 2  # number of direction of motions (flash-left, flash-right)
ntrs = nrep * nstm * ndir
nblocks = 4

if subID == 'test':
    full_screen = False
else:
    full_screen = True
# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file nameTrue
date = sfc.get_date()
time = sfc.get_time()
output_name = f"{subID}_task06_{date}_{time}.json"
# set data directory
save_path = os.path.join("..", "data", "cyc02", output_name)

# --------------------------------
# /// set stimulus parameters

# initialize the display and the keyboard
REF_RATE = 60

# define the flash duration in frames
frame_repeat = 2

# configure the monitor and the stimulus window
mon = sfc.config_mon_dell()
win = sfc.config_win(mon=mon, fullscr=full_screen)
sfc.test_refresh_rate(win, REF_RATE)

# fixation mark
fixdot_radius = .15
FIX_X = 0
FIX_Y = 0

INSTRUCT_DUR = REF_RATE  # duration of the instruction period [frames]

# lines
line_width = 0.12
line_length = 2
line_color = 'black'

# probe
probe_rad = .25
probe_color = 'red'

motion_cycle_dur = REF_RATE  # [frames]
leg_dist = 8  # dva

# # mouse position downsample factor
# mouse_dsf = 20

# potential gap durations (0.5 to 1 sec)
gap_dur_list = range(int(REF_RATE / 2), int(REF_RATE / 1) + 1, 1)

# initialize mouse
mouse = event.Mouse(win=win, visible=False)

# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

# create an equal number of trials per condition (contrast/direction)
dir2_array = np.repeat(['h', 'v'], ntrs / 2)
assert (dir2_array.size == ntrs)
dir1_array = np.tile(np.repeat([-1, 1], int(ntrs / 4)), 2)
assert (dir1_array.size == ntrs)

# randomize the order of each condition array
ind_shuffle = np.arange(ntrs)
np.random.shuffle(ind_shuffle)
dir2_array = dir2_array[ind_shuffle]
dir1_array = dir1_array[ind_shuffle]

# pause trials
pause_array = np.linspace(0, ntrs, nblocks + 1)
pause_array = pause_array[:-1]

# ----------------------------------------------------------------------------
# /// TRIAL BEGINS ///

for itrial in range(5):
    # --------------------------------
    # /// resets

    # reset mouse position
    mouse.setPos((0, 0))

    # reset pse response
    hline_x = np.nan

    # reset loop counter
    loop_cntr = 0

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    # randomly decide on inter-trial interval
    iti = random.choice(gap_dur_list)

    # # add random offset to hline's horizontal onset position
    # hline_x_offset = np.random.choice(np.arange(-hline_size / 2,
    #                                             hline_size / 2, 0.1))

    # --------------------------------
    print('---------------------------')
    print(f'trl: {itrial + 1}')
    print(f'stm: {dir1_array[itrial]}')
    print(f'dir: {dir2_array[itrial]}')

    # --------------------------------
    # /// create visual objects

    # lines
    vline = visual.Rect(win=win,
                        size=(line_width, line_length),
                        fillColor='black')
    hline = visual.Rect(win=win,
                        size=(line_length, line_width),
                        fillColor='black')
    # probe
    probe = visual.Circle(win,
                          radius=probe_rad,
                          pos=(0, 0),
                          fillColor='black')
    # fixation dot
    fixdot1 = visual.Circle(win,
                            radius=fixdot_radius,
                            pos=(FIX_X, FIX_Y),
                            fillColor='black')
    fixdot2 = visual.Circle(win,
                            radius=fixdot_radius * .7,
                            pos=(FIX_X, FIX_Y),
                            fillColor='gray')

    # --------------------------------
    # /// create motion arrays

    npos = int(REF_RATE / frame_repeat / 2)
    if dir1_array[itrial] == 1:
        motionx1_array = np.linspace(-leg_dist, 0, num=npos) / np.sqrt(2)
        motiony1_array = np.linspace(-leg_dist, 0, num=npos) / np.sqrt(2)
        if dir2_array[itrial] == 'h':
            motionx2_array = np.linspace(0, leg_dist, num=npos)
            motiony2_array = np.linspace(0, 0, num=npos)
        if dir2_array[itrial] == 'v':
            motionx2_array = np.linspace(0, 0, num=npos)
            motiony2_array = np.linspace(0, leg_dist, num=npos)
    if dir1_array[itrial] == -1:
        motionx1_array = np.linspace(leg_dist, 0, num=npos) / np.sqrt(2)
        motiony1_array = np.linspace(-leg_dist, 0, num=npos) / np.sqrt(2)
        if dir2_array[itrial] == 'h':
            motionx2_array = np.linspace(0, -leg_dist, num=npos)
            motiony2_array = np.linspace(0, 0, num=npos)
        if dir2_array[itrial] == 'v':
            motionx2_array = np.linspace(0, 0, num=npos)
            motiony2_array = np.linspace(0, leg_dist, num=npos)

    motionx_array = np.concatenate((motionx1_array, motionx2_array))
    motiony_array = np.concatenate((motiony1_array, motiony2_array))

    motionx_array = np.repeat(motionx_array, frame_repeat)
    motiony_array = np.repeat(motiony_array, frame_repeat)

    # --------------------------------
    # /// run the stimulus

    # if itrial in pause_array:
    #     sfc.block_msg(win, np.where(pause_array == itrial)[0][0] + 1, nblocks)

    # gap period
    for igap in range(iti):
        win.flip()

    # motion period
    # loop_flag = True
    # while loop_flag:
    # loop_cntr += 1
    # for imotion in motion_array:

    # # get mouse x-position
    # hline_x = mouse.getPos()[0] / mouse_dsf + hline_x_offset

    for i in range(npos * frame_repeat * 2):
        # draw fixation mark
        fixdot1.draw()
        fixdot2.draw()
        vline.pos = (motionx_array[i]/np.sqrt(2), motiony_array[i]/np.sqrt(2))
        hline.pos = (0, 0)
        vline.draw()
        hline.draw()
        # if imotion == motion_pos1 and loop_cntr > 1:
        #     hline.pos = hline_x, hline_y
        #     box.draw()
        #     vline.draw()
        #     hline.draw()

        win.flip()

    #     # exit loop upon proper response
    #     pressed_key = event.getKeys(keyList=['space', 'escape'])
    #     if 'escape' in pressed_key:
    #         core.quit()
    #     if 'space' in pressed_key:
    #         loop_flag = False
    #         break
    #
    # print(f'PSE: {np.round(hline_x / norm_factor, 2)}')

    # # --------------------------------
    # # /// prepare data for saving
    #
    # # create a dictionary of variables to be saved
    # trial_dict = {'trial_num': itrial + 1,
    #               'stimulus_type': stm_array[itrial],
    #               'postflash_dir': dir_array[itrial],
    #               'pse_x': [np.round(hline_x / norm_factor, 2)],
    #               'loop_count': loop_cntr}
    #
    # # convert to data frame
    # dfnew = pd.DataFrame(trial_dict)
    # # if not first trial, load the existing data frame and concatenate
    # if itrial > 0:
    #     df = pd.read_json(save_path)
    #     dfnew = pd.concat([df, dfnew], ignore_index=True)
    # # save the dataframe
    # dfnew.to_json(save_path)

    # if itrial == ntrs - 1:
    #     sfc.end_screen(win)
# --------------------------------
win.close()
