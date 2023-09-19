"""
Project MIPS-Attention
Mo Shams <MShamsCBR@gmail.com>
Initiated on: June 05, 2023
---

Analyzes data from ECVP23_Exp03
To show the magnitude of the mislocalization of a flashed object at
different times wrt a moving object's sweep

"""
import os
import numpy as np
import pandas as pd
from matplotlib import ticker
import matplotlib.pyplot as plt
from lib import cleanplot as cp
from matplotlib.patches import Polygon

norm_flag = True
# ----------------------------------------------------------------------------

# /// CONFIGURE PATHS AND LOAD DATA ///

data_dir = os.path.join('..', 'data', 'ECVP23_Exp03')
save_dir = os.path.join('..', 'result', 'ECVP23')

file_names = np.array(["AR01_20230227_195314.json",
                       "MS01_20230228_115227.json",
                       "0001_20230601_112438.json",
                       "0005_20230602_105623.json",
                       "0011_20230601_120919.json",
                       "1191_20230602_113813.json",
                       "2002_20230601_105314.json"])

err_mat_x = np.full((file_names.size, 15), fill_value=np.nan)

for ind, file_name in enumerate(file_names):
    subID = file_name[:4]
    file_address = os.path.join(data_dir, file_name)
    df = pd.read_json(file_address)
    # ----------------------------------------------------------------------------

    # /// CONFIGURE DATA ///

    click_locs = df.click_loc.apply(pd.Series)
    probe_locs = df.probe_loc.apply(pd.Series)
    thetas_all = df['movobj_atflash'].to_numpy()
    thetas_all = np.round(thetas_all, 1)
    thetas = np.unique(thetas_all)

    # /// calculate click errors
    errs = click_locs - probe_locs

    # /// assign errors to times
    err_arr_x = np.full(thetas.size, fill_value=np.nan)
    err_arr_y = np.full(thetas.size, fill_value=np.nan)
    counter = -1
    for theta in thetas:
        counter += 1
        ind_loc = thetas_all == theta
        err_arr_x[counter] = np.mean(errs[ind_loc], axis=0)[0]
        err_arr_y[counter] = np.mean(errs[ind_loc], axis=0)[1]

    if norm_flag:
        err_mat_x[ind, :] = err_arr_x / np.max(np.abs(err_arr_x))
    else:
        err_mat_x[ind, :] = err_arr_x
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# /// CONFIGURE PATHS AND LOAD DATA ///

data_dir = os.path.join('..', 'data', 'ECVP23_Exp04')
save_dir = os.path.join('..', 'result', 'ECVP23')

file_names = np.array(["MS01_20230228_115928.json",
                       "0001_20230601_113509.json",
                       "0005_20230602_110336.json",
                       "0011_20230601_121629.json",
                       "1191_20230602_114506.json",
                       "2002_20230601_110153.json"])

err_mat_x_random = np.full((file_names.size, 15), fill_value=np.nan)

for ind, file_name in enumerate(file_names):
    subID = file_name[:4]
    file_address = os.path.join(data_dir, file_name)
    df = pd.read_json(file_address)
    # ------------------------------------------------------------------------

    # /// CONFIGURE DATA ///

    ind_ccw = df.loc[:, 'movobj_dir'] == 'ccw'

    click_locs = df.click_loc.apply(pd.Series)
    probe_locs = df.probe_loc.apply(pd.Series)
    thetas_all = df['movobj_atflash'].to_numpy()

    thetas_all = thetas_all % 360
    thetas_all = np.round(thetas_all, 1)
    thetas = np.unique(thetas_all)
    # convert ccw thetas to cw thetas
    thetas_all[ind_ccw] = 180 - thetas_all[ind_ccw]

    # /// calculate click errors
    errs = click_locs - probe_locs
    # convert ccw error to cw errors
    errs[0][ind_ccw] = -errs[0][ind_ccw]

    # /// assign errors to times
    err_arr_x = np.full(thetas.size, fill_value=np.nan)
    err_arr_y = np.full(thetas.size, fill_value=np.nan)
    counter = -1
    for theta in thetas:
        counter += 1
        ind_loc = thetas_all == theta
        err_arr_x[counter] = np.mean(errs[ind_loc], axis=0)[0]
        err_arr_y[counter] = np.mean(errs[ind_loc], axis=0)[1]

    if norm_flag:
        err_mat_x_random[ind, :] = err_arr_x / np.max(np.abs(err_arr_x))
    else:
        err_mat_x_random[ind, :] = err_arr_x

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# /// CONFIGURE PATHS AND LOAD DATA ///

data_dir = os.path.join('..', 'data', 'ECVP23_Exp05')
save_dir = os.path.join('..', 'result', 'ECVP23')
file_names = np.array(["AR01_20230227_200934.json",
                       "MS01_20230228_120841.json",
                       "0001_20230601_114301.json",
                       "0005_20230602_111038.json",
                       "0011_20230601_122343.json",
                       "1191_20230602_115212.json",
                       "2002_20230601_111050.json"])

err_mat_x_slow = np.full((file_names.size, 15), fill_value=np.nan)

for ind, file_name in enumerate(file_names):
    subID = file_name[:4]
    file_address = os.path.join(data_dir, file_name)
    df = pd.read_json(file_address)
    # ----------------------------------------------------------------------------

    # /// CONFIGURE DATA ///

    click_locs = df.click_loc.apply(pd.Series)
    probe_locs = df.probe_loc.apply(pd.Series)
    thetas_all = df['movobj_atflash'].to_numpy()
    thetas_all = np.round(thetas_all, 1)
    thetas = np.unique(thetas_all)

    # /// calculate click errors
    errs = click_locs - probe_locs

    # /// assign errors to times
    err_arr_x = np.full(thetas.size, fill_value=np.nan)
    err_arr_y = np.full(thetas.size, fill_value=np.nan)
    counter = -1
    for theta in thetas:
        counter += 1
        ind_loc = thetas_all == theta
        err_arr_x[counter] = np.mean(errs[ind_loc], axis=0)[0]
        err_arr_y[counter] = np.mean(errs[ind_loc], axis=0)[1]

    if norm_flag:
        err_mat_x_slow[ind, :] = err_arr_x / np.max(np.abs(err_arr_x))
    else:
        err_mat_x_slow[ind, :] = err_arr_x
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

err_mat_x_mean = np.mean(err_mat_x, 0)
err_mat_x_ste = np.std(err_mat_x, 0) / np.sqrt(err_mat_x.shape[0])

err_mat_x_random_mean = np.mean(err_mat_x_random, 0)
err_mat_x_random_ste = np.std(err_mat_x_random, 0) / np.sqrt(
    err_mat_x_random.shape[0])

err_mat_x_slow_mean = np.mean(err_mat_x_slow, 0)
err_mat_x_slow_ste = np.std(err_mat_x_slow, 0) / np.sqrt(
    err_mat_x_slow.shape[0])

# /// set plot parameters
cp.prep4ai()

# convert theta to time
times = (thetas - 90) / 360 * 1000  # in ms
times_slow = (thetas - 90) / 360 * 2000  # in ms
# create the hypothetical times (x-axis values) for constant-fast to match
# with equivalent positions between fast and slow curves
times_space_matched = (times_slow[-1]/times[-1]) * times

# --------------------------------------

fig, ax = plt.subplots(1, figsize=(5, 4))
fig.suptitle(f"Effect of sweep time (N={file_names.size})")
ax.axhline(color='k', linestyle='--', linewidth=.5)
ax.axvline(color='k', linestyle='--', linewidth=.5)
ax.errorbar(times, err_mat_x_mean, yerr=err_mat_x_ste,
            color='black', label='constant fast')
ax.errorbar(times, err_mat_x_random_mean, yerr=err_mat_x_random_ste,
            color='red', label='random fast')
ax.legend(loc='upper left')
ax.set(xlabel='t(sweep) - t(flash) [ms]',
       xticks=range(-500, 600, 100))
if norm_flag:
    ax.set(ylabel='Normalized mislocalization\nin the direction of motion')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"pop_constant_vs_random_norm.pdf"))
else:
    ax.set(ylabel='Mislocalization\nin the direction of motion [dva]')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"pop_constant_vs_random.pdf"))

# --------------------------------------

fig, ax = plt.subplots(1, figsize=(5, 4))
fig.suptitle(f"Effect of sweep time (N={file_names.size})")
ax.axhline(color='k', linestyle='--', linewidth=.5)
ax.axvline(color='k', linestyle='--', linewidth=.5)
ax.errorbar(times, err_mat_x_mean, yerr=err_mat_x_ste,
            color='black', label='constant fast')
ax.errorbar(times_space_matched, err_mat_x_mean, yerr=err_mat_x_ste,
            color='gray', label='constant fast (spatially matched with slow)')
ax.errorbar(times_slow, err_mat_x_slow_mean, yerr=err_mat_x_slow_ste,
            color='green', label='constant slow')
ax.legend(loc='upper left')
ax.set(xlabel='t(sweep) - t(flash) [ms]',
       xticks=range(-500, 600, 100))
if norm_flag:
    ax.set(ylabel='Normalized mislocalization\nin the direction of motion')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"pop_fast_vs_slow_norm.pdf"))
else:
    ax.set(ylabel='Mislocalization\nin the direction of motion [dva]')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"pop_fast_vs_slow.pdf"))
