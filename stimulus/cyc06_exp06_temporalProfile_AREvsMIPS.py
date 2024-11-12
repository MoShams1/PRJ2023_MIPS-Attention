"""
***** project: PRJ2023_MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Nov 2024

This experiment is to measure the temporal profile of the position shift
evoked by a either a dynamic or a static bar

Stimulus and task procedure:
    A probe flashes at the same location, 15 deg ahead of a bar (
    rotating or static) at different times relative to bar's motion start.
    The bar's motion end at 0 or 180 deg.
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


# disable Panda's false warning message
pd.options.mode.chained_assignment = None  # default='warn'

# ----------------------------------------------------------------------------
# /// INSERT SESSION'S META DATA ///

subID = '123'  # put 'test' for a test run
slow_coeff = 1

# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file name
date = sfc.get_date()
time = sfc.get_time()

output_name = f"cyc06_exp06_{date}_{time}_{subID}.json"

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
motion_halfCycle_dur_ms = 800
motion_dur_frames = int(motion_halfCycle_dur_ms / 1000 * 60 + 1)
motion_dir_base = np.array([-1, 1])
motion_state_base = np.array(['static', 'dynamic'])

probe_rad = .3
probe_color = 'red'
probe_x = 0
probe_y = motion_radius

gap_durations_base = range(int(.75 * refresh_rate),
                           int(1.25 * refresh_rate) + 1, 1)

probe2bar_frame_base = np.arange(-12, 18 + 1, 3)

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

ncnds = 11 * 2 * 2
# probe2bar x motionDirection x motionState

probe2bar_frame_array = np.repeat(probe2bar_frame_base, 2 * 2)
motion_dir_array = np.tile(np.repeat(motion_dir_base, 2), 11)
motion_state_array = np.tile(motion_state_base, 11 * 2)

rep_per_cnd = 10
probe2bar_frame_array = np.repeat(probe2bar_frame_array, rep_per_cnd)
motion_dir_array = np.repeat(motion_dir_array, rep_per_cnd)
motion_state_array = np.repeat(motion_state_array, rep_per_cnd)

ntrials = ncnds * rep_per_cnd
ind_shuffle = np.arange(ntrials)
np.random.shuffle(ind_shuffle)
probe2bar_frame_array = probe2bar_frame_array[ind_shuffle]
motion_dir_array = motion_dir_array[ind_shuffle]
motion_state_array = motion_state_array[ind_shuffle]

assert (probe2bar_frame_array.size == ntrials)
assert (motion_dir_array.size == ntrials)
assert (motion_state_array.size == ntrials)

# ----------------------------------------------------------------------------
# /// CREATE VISUAL OBJECTS ///

probe = visual.Circle(win,
                      radius=probe_rad,
                      fillColor=probe_color,
                      pos=[probe_x, probe_y])

fixdot1 = visual.Circle(win,
                        radius=fixdot_radius,
                        pos=(fixMark_x, fixMark_y),
                        fillColor=fixdot_color)
fixdot2 = visual.Circle(win,
                        radius=fixdot_radius * .7,
                        pos=(fixMark_x, fixMark_y),
                        fillColor=bg_color)

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
    probe2bar_frame = probe2bar_frame_array[itrial]
    probe2bar_ms = probe2bar_frame / refresh_rate * 1000
    motion_dir = motion_dir_array[itrial]
    motion_state = motion_state_array[itrial]
    assert (flash_frame >= probe2bar_frame)

    # /// create motion trajectory array
    bar_thetaArray_base = np.linspace(180, 0,
                                      int((motion_dur_frames + 1) /
                                          frame_repeat))
    bar_thetaArray = np.repeat(bar_thetaArray_base, frame_repeat)

    if motion_dir == -1:
        bar_thetaArray = np.flip(bar_thetaArray)

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
        fixdot1.draw()
        fixdot2.draw()
        win.flip()
        escape_session()

    # post-fixation gap period
    for ifix in range(postFixGap):
        win.flip()

    # motion period at negative SOAs
    if probe2bar_ms < 0 and motion_state == 'dynamic':
        for iprobe in range(frame_repeat):
            for islow in range(slow_coeff):
                if iprobe == 0:
                    probe_on_ms = my_clock.getTime() * 1000
                if iprobe == frame_repeat - 1:
                    probe_off_ms = my_clock.getTime() * 1000
                probe.draw()
                win.flip()
                escape_session()

        for itheta in bar_thetaArray[flash_frame:]:
            for islow in range(slow_coeff):
                if itheta == bar_thetaArray[flash_frame]:
                    bar_on_ms = my_clock.getTime() * 1000
                con_vis.add_bar_polar(win=win,
                                      size=[bar_width, bar_length],
                                      color=bar_color,
                                      theta=itheta,
                                      radius=motion_radius,
                                      x_offset=fixMark_x,
                                      y_offset=fixMark_y)
            win.flip()
            escape_session()
        theta_start = bar_thetaArray[flash_frame]
        theta_end = bar_thetaArray[-1]

    # motion period at positive SOAs
    if probe2bar_ms >= 0 and motion_state == 'dynamic':
        for i in range(len(bar_thetaArray)):
            for islow in range(slow_coeff):
                if i >= (flash_frame - probe2bar_frame):
                    if i == (flash_frame - probe2bar_frame):
                        bar_on_ms = my_clock.getTime() * 1000

                    con_vis.add_bar_polar(win=win,
                                          size=[bar_width, bar_length],
                                          color=bar_color,
                                          theta=bar_thetaArray[i],
                                          radius=motion_radius,
                                          x_offset=fixMark_x,
                                          y_offset=fixMark_y)

                if (i == flash_frame) or (i == flash_frame + 1):
                    if i == flash_frame:
                        probe_on_ms = my_clock.getTime() * 1000
                    probe.draw()

                win.flip()
                escape_session()
                if i == flash_frame + 1:
                    probe_off_ms = my_clock.getTime() * 1000
        theta_start = bar_thetaArray[flash_frame - probe2bar_frame]
        theta_end = bar_thetaArray[-1]

    # bar period at negative SOAs
    if probe2bar_ms < 0 and motion_state == 'static':
        for iprobe in range(frame_repeat):
            for islow in range(slow_coeff):
                if iprobe == 0:
                    probe_on_ms = my_clock.getTime() * 1000
                probe.draw()
                win.flip()
                escape_session()
                if iprobe == frame_repeat - 1:
                    probe_off_ms = my_clock.getTime() * 1000

        for iframe in range(3):
            for islow in range(slow_coeff):
                if iframe == 0:
                    bar_on_ms = my_clock.getTime() * 1000
                con_vis.add_bar_polar(win=win,
                                      size=[bar_width, bar_length],
                                      color=bar_color,
                                      theta=bar_thetaArray[flash_frame],
                                      radius=motion_radius,
                                      x_offset=fixMark_x,
                                      y_offset=fixMark_y)
            win.flip()
            escape_session()
        theta_start = bar_thetaArray[flash_frame]
        theta_end = theta_start

    # bar period at positive SOAs
    if probe2bar_ms >= 0 and motion_state == 'static':
        for i in range(len(bar_thetaArray)):
            for islow in range(slow_coeff):
                if (flash_frame - probe2bar_frame) <= i \
                        < (flash_frame - probe2bar_frame + 3):
                    if i == (flash_frame - probe2bar_frame):
                        bar_on_ms = my_clock.getTime() * 1000

                    con_vis.add_bar_polar(win=win,
                                          size=[bar_width, bar_length],
                                          color=bar_color,
                                          theta=bar_thetaArray[flash_frame],
                                          radius=motion_radius,
                                          x_offset=fixMark_x,
                                          y_offset=fixMark_y)

                if (i == flash_frame) or (i == flash_frame + 1):
                    if i == flash_frame:
                        probe_on_ms = my_clock.getTime() * 1000
                    probe.draw()

                win.flip()
                escape_session()
                if i == flash_frame + 1:
                    probe_off_ms = my_clock.getTime() * 1000
        theta_start = bar_thetaArray[flash_frame - probe2bar_frame]
        theta_end = theta_start

    bar_off_ms = my_clock.getTime() * 1000

    print('---------------------------')
    # # print(f'***last theta: {theta_current} deg***')

    print(f'trial number: {itrial + 1}')
    # print(f'motion direction: {motion_dir}')
    print(f'probe2bar_ms: {probe2bar_ms} ms')

    bar_dur_measured_ms = round(bar_off_ms - bar_on_ms)
    # print(f'Motion duration: {motion_halfCycle_dur_ms} ms')
    print(f'motion_dur_measured_ms: {bar_dur_measured_ms} ms')

    print(f'theta_start: {theta_start}')
    print(f'theta_end: {theta_end}')

    probe_duration_measured = round(probe_off_ms - probe_on_ms)
    print('probe_duration: 33 ms')
    print(f'probe_duration_measured: {probe_duration_measured} ms')

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
                      'probe2bar_ms': probe2bar_ms,
                      'motion_state': motion_state,
                      'theta_start': theta_start,
                      'theta_end': theta_end,
                      'motion_dir': motion_dir,
                      'motion_halfCycle_dur_ms': motion_halfCycle_dur_ms,
                      'bar_dur_measured_ms': bar_dur_measured_ms,
                      'bar_on_ms': bar_on_ms,
                      'bar_off_ms': bar_off_ms,
                      'probe_on_ms': probe_on_ms,
                      'probe_off_ms': probe_off_ms,
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
