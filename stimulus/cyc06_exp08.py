"""
***** project: PRJ2023_MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    March 2025

This experiment is to measure spatiotemporal profile and the role of
attention (endogenous and exogenous) on the position shift induced by a
moving bar.

Stimulus and task procedure:
    A bar moves and probe flashes.
    A spatially informative or an uninformative cue will appear.
    Motion starts -200 to 300 ms after the flash.
    Motion trajectory spans behind, around, or ahead of the flash.
    Subjects locate the probe with a mouse click.

---
To do:

[done] implement SOA>0 (motion after flash)
[done] adjust Trajectory: behind/center/ahead
[doone] cue informative or uninformative
[done] implement SOA=0 (motion with flash)
[dine] implement SOA<0 (motion before flash)
[done] keep one moving bar in two potential locations around two separate
centers: left and right

[] finalize conditions
[] finalize save variables

"""

import os
import random
import warnings
import numpy as np
import pandas as pd
from lib import stim_flow_control as sfc
from psychopy import event, visual, core
from lib import config_visual as con_vis


def get_mouseclick(win, mouse_correctionFactor=1):
    ms_posx = random.choice(np.arange(-2, 2 + .1, .1))
    ms_posy = 0
    mouse = event.Mouse(win=win, visible=True,
                        newPos=[ms_posx * mouse_correctionFactor,
                                ms_posy * mouse_correctionFactor])
    while not mouse.getPressed()[0]:
        escape_session()
        win.flip()
    while mouse.getPressed()[0]:
        pass
    click_loc = mouse.getPos() / mouse_correctionFactor
    click_loc = [round(item, 2) for item in click_loc]
    return click_loc


def escape_session():
    exit_key = event.getKeys(keyList=['escape'])
    if 'escape' in exit_key:
        core.quit()


# disable Panda's false warning message
pd.options.mode.chained_assignment = None  # default='warn'

# ----------------------------------------------------------------------------
# /// INSERT SESSION'S META DATA ///

subID = 'test'  # put 'test' for a test run
slow_coeff = 1

# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file name
date = sfc.get_date()
time = sfc.get_time()

output_name = f"cyc06_exp08_2_{date}_{time}_{subID}.json"

# set data directory
save_path = os.path.join("", "data", "cyc06", output_name)

# --------------------------------
# /// set stimulus parameters

# initialize the display and the keyboard
refresh_rate = 60

# flash duration in frames (motion resolution will change accordingly)
frame_repeat = 2

if subID == 'test':
    full_screen = False
else:
    full_screen = True
bg_color = [-.8, -.8, -.8]
mon = sfc.config_mon_dell()
win = sfc.config_win(mon=mon, fullscr=full_screen, color=bg_color)
sfc.test_refresh_rate(win, refresh_rate)

fixdot_radius = .2
fixMark_x = 0
fixMark_y = 0
fixdot_color = 'white'

bar_width = 0.1
bar_length = 2
bar_color = 'white'
motion_radius = 5
motion_dir_base = np.array([1, 1])
motion_duration_ms_original = 800
motion_duration_frames_original = int(motion_duration_ms_original / 1000 *
                                      refresh_rate + 1)
motion_theta1_original = 150
motion_theta2_original = 30
motion_theta_diff = abs(motion_theta1_original-motion_theta2_original)

probe_rad = .3
probe_color = 'red'
probe_duration_ms = 50
probe_duration_frame = int(probe_duration_ms / 1000 * refresh_rate)
probe_x = 0
probe_y = motion_radius

cue_r = .3
cue_pos_base = np.array([-1, 1])
cue_condition_base = [0, 1]  # uncued/cued
cue_rectangle_mask_width = .6
cue_circle_mask_rad = .2

gap_durations_base = range(int(.75 * refresh_rate),
                           int(1.25 * refresh_rate) + 1, 1)

SOA_ms_base = np.arange(-200, 300 + 1, 100)  # motion after flash

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

# ncnds = 11 * 2
# # probe2bar x motionDirection
#
# SOA_frame_array = np.repeat(SOA_frame_base, 2)
# motion_dir_array = np.tile(motion_dir_base, 11)
#
# rep_per_cnd = 15
# probe2bar_frame_array = np.repeat(SOA_frame_array, rep_per_cnd)
# motion_dir_array = np.repeat(motion_dir_array, rep_per_cnd)
#
# ntrials = ncnds * rep_per_cnd
# ind_shuffle = np.arange(ntrials)
# np.random.shuffle(ind_shuffle)
# probe2bar_frame_array = probe2bar_frame_array[ind_shuffle]
# motion_dir_array = motion_dir_array[ind_shuffle]
#
# assert (probe2bar_frame_array.size == ntrials)
# assert (motion_dir_array.size == ntrials)

ntrials = 100

# ----------------------------------------------------------------------------
# /// CREATE VISUAL OBJECTS ///

probe = visual.Circle(win,
                      radius=probe_rad,
                      fillColor=probe_color)

fixdot1 = visual.Circle(win,
                        radius=fixdot_radius,
                        pos=(fixMark_x, fixMark_y),
                        fillColor=fixdot_color)
fixdot2 = visual.Circle(win,
                        radius=fixdot_radius * .7,
                        pos=(fixMark_x, fixMark_y),
                        fillColor=bg_color)

cue_mark1 = visual.Circle(win,
                          radius=cue_circle_mask_rad,
                          fillColor='lime')
cue_mark2 = visual.Circle(win,
                          radius=cue_circle_mask_rad * .7,
                          fillColor=bg_color)
cue_mark3 = visual.Rect(win=win,
                        size=cue_rectangle_mask_width,
                        fillColor=bg_color,
                        pos=(0, 0))

# ----------------------------------------------------------------------------
# /// OTHER SETTINGS ///

nblocks = 10  # number of blocks
pause_array = np.linspace(0, ntrials, nblocks + 1)
pause_array = pause_array[:-1]

mouse = event.Mouse(win=win, visible=False)

my_clock = core.Clock()

warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------
# /// TRIAL BEGINS ///

for itrial in range(ntrials):

    # --------------------------------
    # /// resets

    mouse.setPos((0, 0))
    mouse.setVisible(False)

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    iti = np.random.choice(gap_durations_base)
    postFixGap = np.random.choice(gap_durations_base)
    flash_frame = 10 * frame_repeat
    # probe2bar_frame = probe2bar_frame_array[itrial]
    # probe2bar_ms = probe2bar_frame / refresh_rate * 1000
    # motion_dir = motion_dir_array[itrial]
    # assert (flash_frame >= probe2bar_frame)

    # SOA_ms = random.choice(SOA_ms_base)
    SOA_ms = -200
    SOA_frame = int(SOA_ms / 1000 * refresh_rate)
    # traj_pos = random.choice([+30, 0, -30])  # behind/center/ahead
    traj_pos = 0
    # motion_dir = random.choice([-1, 1])
    motion_dir = 1
    traj_pos = motion_dir * traj_pos
    motion_side = 1
    cue_side = motion_side
    cue_condition = 1
    side_offset_abs = 5 + random.uniform(-1, 1)  # [dva]
    side_offset = side_offset_abs * motion_side

    probe.pos = fixMark_x + side_offset, fixMark_y + motion_radius

    # --------------------------------
    # /// run stimulus

    # show the block screeen
    if itrial in pause_array:
        sfc.block_msg3(win, np.where(pause_array == itrial)[0][0] + 1,
                       nblocks, color='white')

    # inter-trial interval gap period
    for igap in range(iti):
        win.flip()

    # fixation period
    for ifix in range(int(refresh_rate / 2)):
        fixdot1.draw()
        fixdot2.draw()
        win.flip()
        escape_session()

    # fixation-cue period
    for ifix in range(refresh_rate):
        if cue_condition:
            cue_mark1.pos = cue_side * cue_r, 0
            cue_mark2.pos = cue_side * cue_r, 0
            cue_mark1.draw()
            cue_mark2.draw()
            cue_mark3.draw()
        if not cue_condition:
            cue_mark1.pos = -cue_r, 0
            cue_mark2.pos = -cue_r, 0
            cue_mark1.draw()
            cue_mark2.draw()
            cue_mark1.pos = cue_r, 0
            cue_mark2.pos = cue_r, 0
            cue_mark1.draw()
            cue_mark2.draw()
            cue_mark3.draw()
        fixdot1.draw()
        fixdot2.draw()
        win.flip()
        escape_session()

    # post-fixation gap period
    for ifix in range(postFixGap):
        win.flip()

    # ---------------------------- SOAs > 0
    if SOA_frame > 0:

        # /// create motion trajectory array
        motion_dur_ms = motion_duration_ms_original
        motion_dur_frames = motion_duration_frames_original
        motion_theta1 = motion_theta1_original
        motion_theta2 = motion_theta2_original
        bar_thetaArray_base = np.linspace(motion_theta1 + traj_pos,
                                          motion_theta2 + traj_pos,
                                          int((motion_dur_frames + 1) /
                                              frame_repeat))
        bar_thetaArray = np.repeat(bar_thetaArray_base, frame_repeat)
        if motion_dir == -1:
            bar_thetaArray = np.flip(bar_thetaArray)

        # flash the probe
        probe_on_ms = my_clock.getTime() * 1000
        for isoa in range(probe_duration_frame):
            probe.draw()
            win.flip()

        # pause until motion starts
        for ipause in range(SOA_frame - probe_duration_frame):
            win.flip()

        # move the bar
        motion_start_ms = my_clock.getTime() * 1000
        for imotion in range(len(bar_thetaArray)):
            for islow in range(slow_coeff):
                theta_current = bar_thetaArray[imotion]
                con_vis.add_bar_polar(win=win,
                                      size=[bar_width, bar_length],
                                      color=bar_color,
                                      theta=theta_current,
                                      radius=motion_radius,
                                      x_offset=fixMark_x + side_offset,
                                      y_offset=fixMark_y)
                win.flip()
                escape_session()
        motion_end_ms = my_clock.getTime() * 1000

    # ---------------------------- SOAs <= 0
    if SOA_frame <= 0:

        # /// create motion trajectory array
        motion_dur_ms = motion_duration_ms_original + np.abs(SOA_ms)
        motion_dur_frames = int(motion_dur_ms / 1000 * refresh_rate + 1)
        # adjust starting theta
        motion_theta2 = motion_theta2_original
        motion_theta1 = motion_theta2 + motion_dur_ms / 800 * motion_theta_diff
        bar_thetaArray_base = np.linspace(motion_theta1 + traj_pos,
                                          motion_theta2 + traj_pos,
                                          int((motion_dur_frames + 1) /
                                              frame_repeat))
        bar_thetaArray = np.repeat(bar_thetaArray_base, frame_repeat)
        if motion_dir == -1:
            bar_thetaArray = np.flip(bar_thetaArray)

        iflash = motion_dur_frames - motion_duration_frames_original

        # move the bar
        motion_start_ms = my_clock.getTime() * 1000
        for imotion in range(len(bar_thetaArray)):
            for islow in range(slow_coeff):

                if iflash <= imotion <= iflash+probe_duration_frame:
                    # flash the probe
                    probe_on_ms = my_clock.getTime() * 1000
                    for isoa in range(probe_duration_frame):
                        probe.draw()

                theta_current = bar_thetaArray[imotion]
                con_vis.add_bar_polar(win=win,
                                      size=[bar_width, bar_length],
                                      color=bar_color,
                                      theta=theta_current,
                                      radius=motion_radius,
                                      x_offset=fixMark_x + side_offset,
                                      y_offset=fixMark_y)
                win.flip()
                escape_session()
        motion_end_ms = my_clock.getTime() * 1000

# for i in range(len(bar_thetaArray)):
#     for islow in range(slow_coeff):
#
#         if i >= (flash_frame - probe2bar_frame):
#             if i == (flash_frame - probe2bar_frame):
#                 bar_onset = my_clock.getTime() * 1000
#             if probe2bar_ms < 0:
#                 theta_current = \
#                     bar_thetaArray[i] + 180 - \
#                     bar_thetaArray[flash_frame - probe2bar_frame] - \
#                     90 + motion_dir * 15
#             else:
#                 theta_current = bar_thetaArray[i]
#             con_vis.add_bar_polar(win=win,
#                                   size=[bar_width, bar_length],
#                                   color=bar_color,
#                                   theta=theta_current,
#                                   radius=motion_radius,
#                                   x_offset=fixMark_x,
#                                   y_offset=fixMark_y)
#
#         if (i == flash_frame) or (i == flash_frame + 1):
#             if i == flash_frame:
#                 probe_on_ms = my_clock.getTime() * 1000
#             probe.draw()
#
#         win.flip()
#         escape_session()
#         if i == flash_frame + 1:
#             probe_off_ms = my_clock.getTime() * 1000
# motion_end_ms = my_clock.getTime() * 1000

# print('---------------------------')
# print(f'***last theta: {theta_current} deg***')

# print(f'trial number: {itrial + 1}')
# print(f'motion direction: {motion_dir}')
# print(f'probe2bar_ms: {SOA_ms} ms')

# motion_dur_measured_ms = round(motion_end_ms - motion_start_ms)
# motionVisible_dur_measured_ms = round(motion_end_ms - bar_onset)
# print(f'Motion duration: {motion_dur_ms} ms')
# print(f'motion_dur_measured_ms: {motion_dur_measured_ms} ms')
# print(f'motionVisible_dur_measured_ms: {motionVisible_dur_measured_ms} ms')

# probe_duration_measured = round(probe_off_ms - probe_on_ms)
# print('probe_duration: 33 ms')
# print(f'probe_duration_measured: {probe_duration_measured} ms')

# print(f'bar_thetaStart: {bar_thetaArray[0]} deg')
# print(f'bar_thetaEnd: {bar_thetaArray[-1]} deg')

click_pos = np.round(get_mouseclick(win), 2)
click_err = np.round(click_pos - probe.pos, 2)
# print(f'click position: {click_pos} dva')
print(f'click error: {click_err} dva')

# print(f'motion2probe: {probe_on_ms - motion_start_ms}')

# --------------------------------
# /// save trial parameters

if subID != 'test':

    trial_dict = {'trial_num': itrial + 1,
                  # 'probe2bar_ms': probe2bar_ms,
                  'bar_thetaStart': bar_thetaArray[0],
                  'bar_thetaEnd': bar_thetaArray[-1],
                  'motion_dir': motion_dir,
                  'motion_dur_ms': motion_dur_ms,
                  'motion_start_ms': motion_start_ms,
                  # 'bar_onset': bar_onset,
                  'motion_end_ms': motion_end_ms,
                  'probe_on_ms': probe_on_ms,
                  # 'probe_off_ms': probe_off_ms,
                  'click_pos': [click_pos],
                  'click_xerr': click_err[0],
                  'click_yerr': click_err[1]}

    dfnew = pd.DataFrame(trial_dict)
    if itrial > 0:
        df = pd.read_json(save_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
    dfnew.to_json(save_path)

    if itrial == ntrials - 1:
        sfc.end_screen(win, color='white')

# --------------------------------
win.close()
