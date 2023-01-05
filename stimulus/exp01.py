"""
Project MIPS-Anisotropy – Stimulus – Experiment 01
Mo Shams <MShamsCBR@gmail.com> Jan 03, 2023

In this experiment, my aim is to map the mislocalization of single flashed
probe in the vicinity of a moving object in high resolution.
"""

import os
import numpy as np
from lib import visual, genpath

# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///
save_dir = os.path.join('..', 'data', 'rawdata')

# ----------------------------------------------------------------------------

# /// SESSION META DATA ///

subID = 'test'
NBLOCKS = 1
NTRIALS = 10
screen_num = 0  # 0: primary    1: secondary
frame_rate = 120
full_screen = True

# ----------------------------------------------------------------------------

# /// CONFIGURE VISUAL OBJECTS ///

# /// background
bg_color = 'black'

# /// temporal gap
gap_dur_arr = np.round(np.arange(.5, 1, .1) * frame_rate)  # sec x Hz = frames
gap_dur_arr = gap_dur_arr.astype(int)

# /// fixation dot (function: add_fixdot)
fixdot_size = .7
fixdot_pos = (0, 0)
fixdot_color = 'white'
fixdot_dur = 1 * frame_rate  # sec x Hz = frames

# /// moving object (function: add_movobj; will call gen_path function)
movobj_size = 5
movobj_color = 'white'
movobj_firstpos = (0, 5)
movobj_lastpos = (10, 5)  # two potential last positions
movobj_dur = 1 * frame_rate  # sec x Hz = frames

# /// test grid
grid_width = 12
grid_n = (9, 9)  # number of dots along each dimension

# /// flashing object(s) (function: add_flash)
probe_rad = .25
probe1_color = 'red'
probe2_color = 'Dodgerblue'
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

    # generate motion pathway
    movobj_dir = np.random.choice([-1, 1])
    movobj_pathx, movobj_pathy = \
        genpath.linear(pos1=movobj_firstpos, pos2=movobj_lastpos,
                       dur=movobj_dur)
    if movobj_dir == -1:
        movobj_pathx = -movobj_pathx

    # generate test grid
    grid_x, grid_y = visual.gengrid(width=grid_width, n=grid_n,
                                    movpos1=movobj_firstpos,
                                    movpos2=movobj_lastpos,
                                    movsize=movobj_size,
                                    movdir=movobj_dir)

    # -------------------------------

    # /// run task

    # fixation period
    for frame in range(fixdot_dur):
        visual.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                         color=fixdot_color)
        win.flip()

    # gap period
    for frame in range(firstgap_dur):
        win.flip()

    # motion period
    # todo: make each 'frame' last for k frames
    for iframe in range(movobj_dur):
        visual.addsquare(win=win, width=movobj_size, color=movobj_color,
                         fillcolor=bg_color,
                         pos=(movobj_pathx[iframe], movobj_pathy[iframe]))

        if iframe == movobj_dur / 2:
            visual.addprobe(win=win, radius=probe_rad, color=probe2_color,
                            pos=(0, 0))

            # +++ TEST +++
            # for i in range(grid_n[1]):
            #     for j in range(grid_n[0]):
            #         probe = psychopy.visual.Circle(win, radius=.05,
            #                                        pos=(grid_x[i, j],
            #                                             grid_y[i, j]))
            #         probe.draw()
            # +++++++++++

        win.flip()

    # response period
    # todo: find the same section in ECVP task 3

    # gap period
    for frame in range(lastgap_dur):
        win.flip()

    # -------------------------------

    # /// save data
