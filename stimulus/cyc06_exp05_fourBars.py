"""
***** project: PRJ2023_MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Oct 2024

This experiment is to measure the role of attention on the position shift

Stimulus and task procedure:
    Four probes flash at the vicinity of four moving bars.
    The probes flash at the same location, 15 deg ahead of their corresponding
    bar.
    Bars' motion starts at the same time as the probes flash.
    The bars stop 45 deg after probe's location.
    Subjects locate the probe with a mouse click.

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


def deg2rad(angle):
    return angle / 360 * 2 * np.pi


def pol2cart(rho, phi):
    phi = deg2rad(phi)
    x_cart = rho * np.cos(phi)
    y_cart = rho * np.sin(phi)
    return x_cart, y_cart


# disable Panda's false warning message
pd.options.mode.chained_assignment = None  # default='warn'

# ----------------------------------------------------------------------------
# /// INSERT SESSION'S META DATA ///

subID = 'test'  # put 'test' for a test run
slow_coeff = 5

# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file name
date = sfc.get_date()
time = sfc.get_time()

output_name = f"cyc06_exp05_{date}_{time}_{subID}.json"

# set data directory
save_path = os.path.join("..", "data", "cyc06", output_name)

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
motion_dur_ms = 800
motion_dur_frames = int(motion_dur_ms / 1000 * 60 + 1)
motion_dir_base = np.array([-1, 1])

probe_rad = .3
probe_color = 'red'
probe_r = motion_radius
probe1_theta = 0
probe2_theta = 90
probe3_theta = 180
probe4_theta = 270

cue_rad = .3
cue_r = .3
cue_theta_base = [0, 90, 180, 270]
cue_condition_base = [0, 1]  # uncued (cue before motion) vs. cued (cue after
# motion)
cue_rectangle_mask_width = .6
cue_circle_mask_rad = .2
gap_durations_base = range(int(.75 * refresh_rate),
                           int(1.25 * refresh_rate) + 1, 1)

# probe2bar_frame_base = np.arange(-12, 18 + 1, 3)
# ----------------------------------------------------------------------------
# /// CONDITIONS ///

ncnds = 11 * 2
# probe2bar x motionDirection

# probe2bar_frame_array = np.repeat(probe2bar_frame_base, 2)
motion_dir_array = np.tile(motion_dir_base, 11)

rep_per_cnd = 15
# probe2bar_frame_array = np.repeat(probe2bar_frame_array, rep_per_cnd)
motion_dir_array = np.repeat(motion_dir_array, rep_per_cnd)

ntrials = ncnds * rep_per_cnd
ind_shuffle = np.arange(ntrials)
np.random.shuffle(ind_shuffle)
# probe2bar_frame_array = probe2bar_frame_array[ind_shuffle]
motion_dir_array = motion_dir_array[ind_shuffle]

# assert (probe2bar_frame_array.size == ntrials)
assert (motion_dir_array.size == ntrials)

# ----------------------------------------------------------------------------
# /// CREATE VISUAL OBJECTS ///

probe1 = visual.Circle(win,
                       radius=probe_rad,
                       fillColor=probe_color,
                       pos=pol2cart(probe_r, probe1_theta))
probe2 = visual.Circle(win,
                       radius=probe_rad,
                       fillColor=probe_color,
                       pos=pol2cart(probe_r, probe2_theta))
probe3 = visual.Circle(win,
                       radius=probe_rad,
                       fillColor=probe_color,
                       pos=pol2cart(probe_r, probe3_theta))
probe4 = visual.Circle(win,
                       radius=probe_rad,
                       fillColor=probe_color,
                       pos=pol2cart(probe_r, probe4_theta))

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
                          fillColor='green')
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
    flash_frame = 10 * frame_repeat  # to make probe 15 deg ahead
    bar_offset = 16 * frame_repeat  # to make bar disappear 30 deg after
    probe2bar_frame = 0
    cue_theta = 0
    cue_condition = 1
    probe2bar_ms = probe2bar_frame / refresh_rate * 1000

    assert (flash_frame >= probe2bar_frame)

    # /// create motion trajectory array
    bar_thetaArray_base = np.linspace(90, - 90,
                                      int((motion_dur_frames + 1) /
                                          frame_repeat))
    bar_thetaArray = np.repeat(bar_thetaArray_base, frame_repeat)

    theta_current = np.full(4, np.nan)
    motion_dir = [-1, -1, 1, 1]
    np.random.shuffle(motion_dir)
    if motion_dir[0] == -1:
        bar1_thetaArray = np.flip(bar_thetaArray + probe1_theta)
    else:
        bar1_thetaArray = bar_thetaArray + probe1_theta
    if motion_dir[1] == -1:
        bar2_thetaArray = np.flip(bar_thetaArray + probe2_theta)
    else:
        bar2_thetaArray = bar_thetaArray + probe2_theta
    if motion_dir[2] == -1:
        bar3_thetaArray = np.flip(bar_thetaArray + probe3_theta)
    else:
        bar3_thetaArray = bar_thetaArray + probe3_theta
    if motion_dir[3] == -1:
        bar4_thetaArray = np.flip(bar_thetaArray + probe4_theta)
    else:
        bar4_thetaArray = bar_thetaArray + probe4_theta

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
    for ifix in range(refresh_rate):
        if cue_condition:
            cue_mark1.pos = pol2cart(cue_r, cue_theta)
            cue_mark2.pos = pol2cart(cue_r, cue_theta)
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

    motion_start_ms = my_clock.getTime() * 1000

    for i in range(len(bar_thetaArray)):
        for islow in range(slow_coeff):

            if i >= (flash_frame - probe2bar_frame):
                if i == (flash_frame - probe2bar_frame):
                    bar_onset = my_clock.getTime() * 1000
                if probe2bar_ms < 0:
                    theta_current = bar_thetaArray[i] + \
                                    180 - \
                                    bar_thetaArray[flash_frame -
                                                   probe2bar_frame] - \
                                    90 + \
                                    motion_dir * 15
                else:
                    theta_current[0] = bar1_thetaArray[i]
                    theta_current[1] = bar2_thetaArray[i]
                    theta_current[2] = bar3_thetaArray[i]
                    theta_current[3] = bar4_thetaArray[i]

                if i <= bar_offset:
                    for ibar in range(4):
                        con_vis.add_bar_polar(win=win,
                                              size=[bar_width, bar_length],
                                              color=bar_color,
                                              theta=theta_current[ibar],
                                              radius=motion_radius,
                                              x_offset=fixMark_x,
                                              y_offset=fixMark_y)

            if (i == flash_frame) or (i == flash_frame + 1):
                if i == flash_frame:
                    probe_on_ms = my_clock.getTime() * 1000
                probe1.draw()
                probe2.draw()
                probe3.draw()
                probe4.draw()

            win.flip()
            escape_session()
            if i == flash_frame + 1:
                probe_off_ms = my_clock.getTime() * 1000

    motion_end_ms = my_clock.getTime() * 1000

    for ifix in range(refresh_rate):
        cue_mark1.pos = pol2cart(cue_r, cue_theta)
        cue_mark2.pos = pol2cart(cue_r, cue_theta)
        cue_mark1.draw()
        cue_mark2.draw()
        cue_mark3.draw()
        fixdot1.draw()
        fixdot2.draw()
        win.flip()
        escape_session()

    print('---------------------------')
    print(f'trial number: {itrial + 1}')
    # print(f'motion direction: {motion_dir}')
    print(f'probe2bar_ms: {probe2bar_ms} ms')

    motion_dur_measured_ms = round(motion_end_ms - motion_start_ms)
    motionVisible_dur_measured_ms = round(motion_end_ms - bar_onset)
    # print(f'Motion duration: {motion_dur_ms} ms')
    print(f'motion_dur_measured_ms: {motion_dur_measured_ms} ms')
    print(f'motionVisible_dur_measured_ms: {motionVisible_dur_measured_ms} ms')

    probe_duration_measured = round(probe_off_ms - probe_on_ms)
    print('probe_duration: 33 ms')
    print(f'probe_duration_measured: {probe_duration_measured} ms')

    # print(f'bar_thetaStart: {bar2_thetaArray[0]} deg')
    # print(f'bar_thetaEnd: {bar2_thetaArray[-1]} deg')

    click_pos = np.round(get_mouseclick(win), 2)
    probe.pos =
    click_err_norm = np.round(click_pos - probe.pos, 2)
    # print(f'click position: {click_pos} dva')
    # print(f'click error: {click_err} dva')

    # print(f'motion2probe: {probe_on_ms - motion_start_ms}')

    # --------------------------------
    # /// save trial parameters

    # if subID != 'test':
    #
    #     trial_dict = {'trial_num': itrial + 1,
    #                   'probe2bar_ms': probe2bar_ms,
    #                   'bar_thetaStart': bar_thetaArray[0],
    #                   'bar_thetaEnd': bar_thetaArray[-1],
    #                   'motion_dir': motion_dir,
    #                   'motion_dur_ms': motion_dur_ms,
    #                   'motion_start_ms': motion_start_ms,
    #                   'bar_onset': bar_onset,
    #                   'motion_end_ms': motion_end_ms,
    #                   'probe_on_ms': probe_on_ms,
    #                   'probe_off_ms': probe_off_ms,
    #                   'click_pos': [click_pos],
    #                   'click_xerr': click_err[0],
    #                   'click_yerr': click_err[1]}
    #
    #     dfnew = pd.DataFrame(trial_dict)
    #     if itrial > 0:
    #         df = pd.read_json(save_path)
    #         dfnew = pd.concat([df, dfnew], ignore_index=True)
    #     dfnew.to_json(save_path)
    #
    #     if itrial == ntrials - 1:
    #         sfc.end_screen(win, color='white')

# --------------------------------
win.close()
