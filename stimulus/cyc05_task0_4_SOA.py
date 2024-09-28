"""
***** project: PRJ2023_MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Sep 2024

todo: update description
Task Procedure:
    A vertical bar starts at the center and above the fixation dot and moves
    either righward or leftward.
    A probe flashes at 250 ms ahead of the bar.
    The probe flashes at xoffsets of -1 and 1 dva.
    The bar-probe SOA varies from -700 to 700 ms in 50 ms steps.

"""

import os
import random
import warnings
import numpy as np
import pandas as pd
from lib import stim_flow_control as sfc
from psychopy import event, visual, core


def get_mouseclick(win, mouse_correctionFactor=1):
    ms_posx = random.choice(range(-2, 2 + 1))
    ms_posy = random.choice(range(-2, 2 + 1))
    mouse = event.Mouse(win=win, visible=True,
                        newPos=[ms_posx * mouse_correctionFactor,
                                ms_posy * mouse_correctionFactor])
    while not mouse.getPressed()[0]:
        escape_session()  # force exit with 'escape' button
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

subID = 'test'  # subject ID (put 'test' for a test run)
slow_coeff = 2  # on dell:1 | on mac:2

if subID == 'test':
    full_screen = False
else:
    full_screen = True
# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file name
date = sfc.get_date()
time = sfc.get_time()

output_name = f"cyc05_task0_3_{date}_{time}_{subID}.json"

# set data directory
save_path = os.path.join("..", "data", "cyc05", output_name)

# --------------------------------
# /// set stimulus parameters

# initialize the display and the keyboard
REF_RATE = 60

# define the flash duration in frames
frame_repeat = 2

# configure the monitor and the stimulus window
bg_color = [-.8, -.8, -.8]
mon = sfc.config_mon_dell()
win = sfc.config_win(mon=mon, fullscr=full_screen, color=bg_color)
sfc.test_refresh_rate(win, REF_RATE)

# fixation mark
fixdot_radius = .16
FIX_X = 0
FIX_Y = -2
fixdot_color = 'white'

# probe
probe_rad = .25
probe_color = 'red'
probe2bar_distance_ms = 250
probe_xoffset_base_dva = np.array([-1, 1])
probe_yoffset = 4

# lines
line_width = 0.2
vline_length = 2
line_color = 'white'
line_vel = 10  # dva/s
line_start_ypos = 4  # dva
line_end_ypos = 4  # dva
postFlashMotion_ms = 500
postFlashMotion_frame = int(postFlashMotion_ms / 1000 * REF_RATE)
motion_dir_base = np.array([-1, 1])

# probe-line relation
bar1probe_soa_ms = 100

# bar1-bar2 relation
bar12soa_base_ms = np.array(range(-200, 200 + 1, 50))
bar12soa_base_ms = np.append(bar12soa_base_ms, 999)

# potential gap durations (0.75 - 1.25 sec)
gap_durations_base = range(int(REF_RATE * .75), int(REF_RATE * 1.25) + 1, 1)

# ----------------------------------------------------------------------------
# /// CONDITIONS ///

ncnds = 10 * 2 * 2
# SOA x probeX x motionDirection

bar12soa_array_ms = np.repeat(bar12soa_base_ms, 2 * 2)
probe_xoffset_array_dva = np.tile(np.repeat(probe_xoffset_base_dva, 2), 10)
motion_dir_array = np.tile(motion_dir_base, 10 * 2)

rep_per_cnd = 2
bar12soa_array_ms = np.repeat(bar12soa_array_ms, rep_per_cnd)
probe_xoffset_array_dva = np.repeat(probe_xoffset_array_dva, rep_per_cnd)
motion_dir_array = np.repeat(motion_dir_array, rep_per_cnd)

ntrials = ncnds * rep_per_cnd
ind_shuffle = np.arange(ntrials)
np.random.shuffle(ind_shuffle)
bar12soa_array_ms = bar12soa_array_ms[ind_shuffle]
probe_xoffset_array_dva = probe_xoffset_array_dva[ind_shuffle]
motion_dir_array = motion_dir_array[ind_shuffle]

assert (bar12soa_array_ms.size == ntrials)
assert (probe_xoffset_array_dva.size == ntrials)
assert (motion_dir_array.size == ntrials)

# ----------------------------------------------------------------------------
# /// CREATE VISUAL OBJECTS ///

# line
vline = visual.Rect(win=win,
                    size=(line_width, vline_length),
                    fillColor=line_color)

vline2 = visual.Rect(win=win,
                     size=(line_width, vline_length),
                     fillColor=line_color)

# probe
probe = visual.Circle(win,
                      radius=probe_rad,
                      pos=[0, 0],
                      fillColor=probe_color)

# fixation dot
fixdot1 = visual.Circle(win,
                        radius=fixdot_radius,
                        pos=(FIX_X, FIX_Y),
                        fillColor=fixdot_color)
fixdot2 = visual.Circle(win,
                        radius=fixdot_radius * .7,
                        pos=(FIX_X, FIX_Y),
                        fillColor=bg_color)

# ----------------------------------------------------------------------------
# /// OTHER SETTINGS ///

# pause trials
nblocks = 4  # number of blocks
pause_array = np.linspace(0, ntrials, nblocks + 1)
pause_array = pause_array[:-1]

# initialize mouse
mouse = event.Mouse(win=win, visible=False)

# initialize clock
my_clock = core.Clock()

# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------
# /// TRIAL BEGINS ///

for itrial in range(ntrials):

    # --------------------------------
    # /// resets

    # reset mouse position
    mouse.setPos((0, 0))
    mouse.setVisible(False)

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    iti = np.random.choice(gap_durations_base)
    postFixGap = np.random.choice(gap_durations_base)
    bar12soa_ms = int(bar12soa_array_ms[itrial])
    bar12soa_frame = int(bar12soa_ms / 1000 * REF_RATE)
    bar1probe_soa_frame = bar1probe_soa_ms / 1000 * REF_RATE
    # soa_dva = soa_ms / 1000 * line_vel
    motion_dir = motion_dir_array[itrial]
    xshift_steps = line_vel / REF_RATE * frame_repeat
    probe_xoffset = probe_xoffset_array_dva[itrial]

    line_start_xpos = probe_xoffset - \
                      (line_vel * probe2bar_distance_ms / 1000) - \
                      (line_vel * bar1probe_soa_ms / 1000)

    motion_dur_frames = bar1probe_soa_frame + postFlashMotion_frame

    print('---------------------------')
    print(f'trial number    : {itrial + 1}')
    print(f'motion direction: {motion_dir}')

    # --------------------------------
    # /// create motion trajectory array
    line_end_xpos = (motion_dur_frames / frame_repeat * xshift_steps) + \
                    line_start_xpos

    motionX_array = np.linspace(line_start_xpos,
                                line_end_xpos,
                                num=int(motion_dur_frames / frame_repeat))
    motionX_array = motionX_array * motion_dir

    motionY_array = np.linspace(line_start_ypos,
                                line_end_ypos,
                                num=int(motion_dur_frames / frame_repeat))

    motionX_array = np.repeat(motionX_array, frame_repeat)
    motionY_array = np.repeat(motionY_array, frame_repeat)

    # /// bar2 motion frames
    bar2_frames = [bar12soa_frame, bar12soa_frame + 1, bar12soa_frame + 2,
                   bar12soa_frame + 3, bar12soa_frame + 4, bar12soa_frame + 5]

    # /// bar2 motion array
    line2_start_xpos = probe_xoffset + \
                       (line_vel * probe2bar_distance_ms / 1000)
    line2_motion_array = [line2_start_xpos,
                          line2_start_xpos - xshift_steps,
                          line2_start_xpos - 2 * xshift_steps]
    line2_motion_array = np.repeat(line2_motion_array, 2)
    line2_motion_array = line2_motion_array * motion_dir

    # /// update probe position according to motion direction
    probe.pos = [probe_xoffset * motion_dir, probe_yoffset]

    # --------------------------------
    # /// run stimulus

    # show the block screeen
    if itrial in pause_array:
        sfc.block_msg2(win, np.where(pause_array == itrial)[0][0] + 1,
                       nblocks, color='white')

    # inter-trial interval gap period
    for igap in range(iti):
        win.flip()

    # fixation period
    for ifix in range(REF_RATE):
        fixdot1.draw()
        fixdot2.draw()
        win.flip()
        escape_session()

    # post-fixation gap period
    for ifix in range(postFixGap):
        win.flip()

    # move the vertical bar & flash the probe
    my_clock.reset()
    probe_time = np.nan
    if (bar12soa_ms < 0) & (bar12soa_ms != 999):
        line2_time = my_clock.getTime() * 1000
        for iline2 in range(3):
            vline2.draw()
        for i in range(bar12soa_frame):
            win.flip()

    motion_start_time = my_clock.getTime() * 1000
    for i in range(len(motionX_array)):
        for islow in range(slow_coeff):
            vline.pos = (motionX_array[i], motionY_array[i])
            vline.draw()

            # draw line2
            if (i in bar2_frames) & (bar12soa_ms != 999):
                bar2_iframe = bar2_frames.index(i)
                vline2.pos = [line2_motion_array[bar2_iframe],
                              motionY_array[i]]
                vline2.draw()

            # flash the probe
            if i == bar1probe_soa_frame:
                probe.draw()
                probe_time = my_clock.getTime() * 1000

            win.flip()

    # motion_end_ms = my_clock.getTime() * 1000
    # motion_dur_measured_ms = motion_end_ms - motion_start_time
    # soa_measured_ms = probe_time - motion_start_time
    # flash2motionEnd_measured_ms = motion_end_ms - probe_time
    # print(f'SOA: {bar12soa_ms} ms')
    # print(f'SOA measured: {round(soa_measured_ms, 2)} ms')
    # print(f'Motion duration measured: {round(motion_dur_measured_ms, 2)} ms')
    # print(f'Flash-BarEnd measured:'
    #       f' {round(flash2motionEnd_measured_ms, 2)} ms')
    # motion_distance = abs(motionX_array[-1] - motionX_array[0])
    # motion_vel_measured = abs(motion_distance) / motion_dur_measured_ms * 1000
    # print(f'Motion velocity: {round(motion_vel_measured, 2)} dva/s')
    # print(f'probe hor. position  : {probe_xoffset} dva')
    # print(f'probe-bar temp. dist.: {probe2bar_distance_ms} ms')
    #
    click_pos = np.round(get_mouseclick(win), 2)
    # click_err = np.round(click_pos - probe.pos, 2)
    # print(f'click position  : {click_pos} dva')
    # print(f'click error     : {click_err} dva')
    #
    # # --------------------------------
    # # /// save trial parameters
    #
    # trial_dict = {'trial_num': itrial + 1,
    #               'soa_ms': soa_ms,
    #               'soa_ms_measured': soa_measured_ms,
    #               'probe_pos': [probe.pos],
    #               'flash2barEnd_measured_ms': flash2motionEnd_measured_ms,
    #               'probe2bar_distance_ms': probe2bar_distance_ms,
    #               'motion_dir': motion_dir,
    #               'motion_duration_ms_measure': motion_dur_measured_ms,
    #               'motion_vel_measured': motion_vel_measured,
    #               'motion_xstart': motionX_array[0],
    #               'motion_xend': motionX_array[-1],
    #               'motion_ystart': line_start_ypos,
    #               'motion_yend': line_end_ypos,
    #               'click_pos': [click_pos],
    #               'click_xerr': click_err[0],
    #               'click_yerr': click_err[1]}
    #
    # dfnew = pd.DataFrame(trial_dict)
    # # if not first trial, load the existing data frame and concatenate
    # if itrial > 0:
    #     df = pd.read_json(save_path)
    #     dfnew = pd.concat([df, dfnew], ignore_index=True)
    # dfnew.to_json(save_path)
    #
    # if itrial == ntrials - 1:
    #     sfc.end_screen(win, color='white')

# --------------------------------
win.close()
