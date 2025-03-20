"""
***** project: PRJ2023_MIPS-Attention

    Mohammad Shams <m.shams.ahmar@gmail.com>
    Oct 2024

This experiment is to replicate Watanabe et al. 2003/2005

Task Procedure:
    A bar rotates for 180 deg around the center.
    A probe flashes at the same location, at different times relative to bar's
    motion start.

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

subID = '0000'  # put 'test' for a test run
slow_coeff = 1

# ----------------------------------------------------------------------------
# /// CONFIGURATION ///

# create file name
date = sfc.get_date()
time = sfc.get_time()

output_name = f"cyc06_exp01_{date}_{time}_{subID}.json"

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

fixdot_radius = .4
fixMark_x = 0
fixMark_y = 0
fixdot_color = 'white'

bar_width = 0.2
bar_length = 5
bar_color = 'white'
motion_path_radius = 8
motion_dur_ms = 800
motion_dur_frames = int(motion_dur_ms / 1000 * 60 + 1)
motion_dir_base = np.array([-1, 1])

probe_rad = .6
probe_color = 'red'
theta_offset = 150
probe_theta = 90 + theta_offset
probe_x, probe_y = pol2cart(motion_path_radius, probe_theta)
gap_durations_base = range(int(.75 * refresh_rate),
                           int(1.25 * refresh_rate) + 1, 1)

flash_frame_array = [10, 10, 10, 20, 20, 20]

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

mouse = event.Mouse(win=win, visible=False)

my_clock = core.Clock()

warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------
# /// TRIAL BEGINS ///

for itrial in range(len(flash_frame_array)):

    # --------------------------------
    # /// resets

    mouse.setPos((0, 0))
    mouse.setVisible(False)

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    iti = np.random.choice(gap_durations_base)
    postFixGap = np.random.choice(gap_durations_base)
    flash_frame = flash_frame_array[itrial] * frame_repeat

    # /// create motion trajectory array
    bar_thetaArray_base = np.linspace(180, 0,
                                      int((motion_dur_frames + 1) /
                                          frame_repeat)) + theta_offset
    bar_thetaArray = np.repeat(bar_thetaArray_base, frame_repeat)

    # --------------------------------
    # /// run stimulus

    # inter-trial interval gap period
    for igap in range(60):
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

    motion_start_ms = my_clock.getTime() * 1000

    for i in range(len(bar_thetaArray)):
        for islow in range(slow_coeff):

            con_vis.add_bar_polar(win=win,
                                  size=[bar_width, bar_length],
                                  color=bar_color,
                                  theta=bar_thetaArray[i],
                                  radius=motion_path_radius,
                                  x_offset=fixMark_x,
                                  y_offset=fixMark_y)

            if (i == flash_frame) or (i == flash_frame + 1):
                if i == flash_frame:
                    probe_on_ms = my_clock.getTime() * 1000
                    probe2bar_deg = (bar_thetaArray[i] - probe_theta)
                probe.draw()

            win.flip()
            escape_session()
            if i == flash_frame + 1:
                probe_off_ms = my_clock.getTime() * 1000

    motion_end_ms = my_clock.getTime() * 1000

    for i in range(10):
        con_vis.add_bar_polar(win=win,
                              size=[bar_width, motion_path_radius],
                              color='green',
                              theta=probe_theta,
                              radius=motion_path_radius/2,
                              x_offset=fixMark_x,
                              y_offset=fixMark_y)
        win.flip()

    print('---------------------------')
    print(f'trial number    : {itrial + 1}')
    # print(f'motion direction: {motion_dir}')
    print(f'probe2bar_deg: {round(probe2bar_deg, 2)} deg')

    motion_dur_measured_ms = round(motion_end_ms - motion_start_ms)
    # print(f'Motion duration: {motion_dur_ms} ms')
    print(f'Motion duration measured: {motion_dur_measured_ms} ms')

    probe_duration_measured = round(probe_off_ms - probe_on_ms)
    print('Probe duration: 33 ms')
    print(f'Probe duration measured: {probe_duration_measured} ms')

    # print(f'bar_thetaStart: {bar_thetaArray[0]} deg')
    # print(f'bar_thetaEnd: {bar_thetaArray[-1]} deg')

# --------------------------------
win.close()
