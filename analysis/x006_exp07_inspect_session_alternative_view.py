"""
***** Project MIPS-Anisotropy
***** Analysis of experiment 06

        Mo Shams <MShamsCBR@gmail.com>
        Jan 24, 2023

To inspect each session of experiment 7, where multiple probe positions were
tested along the moving trajectory of the moving object either reverses at
its midway or continues in its original direction, besides, the time between
the flash and the reversal varied.

"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lib import cleanplot as cp

# ----------------------------------------------------------------------------

# /// FUNCTIONS ///


# ----------------------------------------------------------------------------

# /// CONFIGURE PATHS AND LOAD DATA ///

data_dir = os.path.join('..', 'data', 'exp07', 'raw')
save_dir = os.path.join('..', 'result', 'exp07')
file_name = "MS1_20230124_131000_random.json"
subID = file_name[:3]
file_address = os.path.join(data_dir, file_name)
df = pd.read_json(file_address)
# ----------------------------------------------------------------------------

# /// CONFIGURE DATA ///

# /// extract visual object and response locations
movobj_pos1 = df.movobj_firstpos.apply(pd.Series)[0]
movobj_pos2 = df.movobj_lastpos.apply(pd.Series)[0]
probe_locs = df.probe_loc.apply(pd.Series)
click_locs = df.click_loc.apply(pd.Series)
movobj_flash_pos = df.movobj_posatflash.apply(pd.Series)[0].unique()
movobj_flash_pos = np.sort(movobj_flash_pos)
iframe_flash_arr = df.iframe_flash.unique()
iframe_flash_arr = np.sort(iframe_flash_arr)
rel_flash_time = [-200, -100, 0, 100, 200]
# /// horizontally flip the probe and click locations from leftward coditions
msk_rightward = movobj_pos1 < 0
msk_leftward = movobj_pos1 > 0
click_locs.loc[msk_leftward, 0] = -click_locs.loc[msk_leftward, 0]
probe_locs.loc[msk_leftward, 0] = -probe_locs.loc[msk_leftward, 0]

# /// calculate click errors
errs = click_locs - probe_locs

# /// mask conditions
msk_reversed = movobj_pos1 == movobj_pos2
msk_passed = movobj_pos1 != movobj_pos2

# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

cp.prep4ai()

# @@@ plot magnitude of the mislocalization across conditions
fig, ax = plt.subplots(1, 5, figsize=(20, 5), sharey=True)
fig.suptitle(f"subID: {subID} – Randomized Order")

for isubplot in range(5):

    msk_time = df.iframe_flash == iframe_flash_arr[isubplot]

    # /// extract erros in each condition
    err_mat_passed = np.full((4, 11), np.nan)
    err_mat_reversed = np.full((4, 11), np.nan)
    probex_arr = np.array(sorted(probe_locs[0].unique()))
    for iprobe, probex in enumerate(probex_arr):
        err_mat_passed[:, iprobe] = \
            errs[(probe_locs[0] == probex) & msk_passed & msk_time][0]
        err_mat_reversed[:, iprobe] = errs[(probe_locs[0] == probex) &
                                           msk_reversed & msk_time][0]

    # ax[isubplot].axhline(color='grey')
    movobj_center = movobj_flash_pos[isubplot]
    ax[isubplot].plot(0, -3, '+', markersize=10, mec='black')
    ax[isubplot].plot([movobj_center - 2.5, movobj_center + 2.5],
                      [-2.5, -2.5], color='black', linewidth=3)
    if isubplot > 2:
        movobj_center_reverse = - movobj_center
    else:
        movobj_center_reverse = movobj_center
    ax[isubplot].plot(
        [movobj_center_reverse - 2.5,
         movobj_center_reverse + 2.5],
        [-2.7, -2.7], color='red', linewidth=3)

    line_passed, = ax[isubplot].plot(probex_arr - movobj_center,
                                     err_mat_passed.mean(axis=0),
                                     color='black')
    ax[isubplot].plot(np.tile(probex_arr - movobj_center,
                              err_mat_passed.shape[0]),
                      err_mat_passed.flatten(),
                      'o', mec='black', mfc='none')
    line_reversed, = ax[isubplot].plot(probex_arr - movobj_center,
                                       err_mat_reversed.mean(axis=0),
                                       color='red')
    ax[isubplot].plot(np.tile(probex_arr - movobj_center,
                              err_mat_reversed.shape[0]),
                      err_mat_reversed.flatten(),
                      'o', mec='red', mfc='none')
    ax[isubplot].set(xticks=probex_arr - movobj_center,
                     xlim=[np.min(probex_arr - movobj_center) - 2,
                           np.max(probex_arr - movobj_center) + 2],
                     xlabel="Probe's horizontal distance from midpoint ("
                            "pass/reverse) [dva]",
                     ylabel="Mislocalization in direction of motion [dva]",
                     title=f"Flash time wrt mid"
                           f"point: {rel_flash_time[isubplot]} ms")
    leg = ax[isubplot].legend([line_passed, line_reversed],
                              ['Passing trj.', 'Reversive trj.'])
    leg.get_frame().set_linewidth(0)
    cp.trim_spines(ax[isubplot])
    plt.tight_layout()

# plt.savefig(os.path.join(save_dir, f"{subID}.pdf"))
