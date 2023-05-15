"""
***** Project MIPS-SProf
***** Analysis of experiment 06

        Mo Shams <MShamsCBR@gmail.com>
        Jan 23, 2023

To inspect each session of experiment 6, where multiple probe positions were
tested along the moving trajectory of the moving object either reverses at
its midway or continues in its original direction.

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

data_dir = os.path.join('..', 'data', 'exp06', 'raw')
save_dir = os.path.join('..', 'result', 'exp06')
file_name = "test_20230123_211141_random.json"
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

# /// extract erros in each condition
err_mat_passed = np.full((4, 11), np.nan)
err_mat_reversed = np.full((4, 11), np.nan)
probex_arr = sorted(probe_locs[0].unique())
for iprobe, probex in enumerate(probex_arr):
    err_mat_passed[:, iprobe] = errs[(probe_locs[0] == probex) & msk_passed][0]
    err_mat_reversed[:, iprobe] = errs[(probe_locs[0] == probex) &
                                       msk_reversed][0]
# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

cp.prep4ai()

# @@@ plot magnitude of the mislocalization across conditions
fig, ax = plt.subplots(1, figsize=(4, 4), sharey=True)
fig.suptitle(f"subID: {subID} – Blocked Order")
ax.axhline(color='grey')
line_passed, = ax.plot(probex_arr, err_mat_passed.mean(axis=0), color='black')
ax.plot(np.tile(probex_arr, err_mat_passed.shape[0]),
        err_mat_passed.flatten(), 'o', mec='black', mfc='none')
line_reversed, = ax.plot(probex_arr, err_mat_reversed.mean(axis=0),
                         color='red')
ax.plot(np.tile(probex_arr, err_mat_reversed.shape[0]),
        err_mat_reversed.flatten(), 'o', mec='red', mfc='none')
ax.set(xticks=probex_arr,
       xlim=[np.min(probex_arr) - 1, np.max(probex_arr) + 1],
       xlabel="Probe's horizontal distance from midpoint (pass/reverse) [deg]",
       ylabel="Mislocalization in direction of motion [deg]")
leg = ax.legend([line_passed, line_reversed],
                ['Passing trj.', 'Reversive trj.'])
leg.get_frame().set_linewidth(0)
cp.trim_spines(ax)
plt.tight_layout()

plt.savefig(os.path.join(save_dir, f"{subID}_pass_vs_reverse_blocked.pdf"))
