"""
***** Project PRJ2023_MIPS-Attention
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
file_name = "MS1_20230124_184144_random_control.json"
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
movobj_flash_pos_all = df.movobj_posatflash.apply(pd.Series)[0]
movobj_flash_pos = np.sort(movobj_flash_pos_all.unique())
iframe_flash_arr = df.iframe_flash.unique()
iframe_flash_arr = np.sort(iframe_flash_arr)
rel_flash_time = [-200, -100, 0, 100, 200]

# /// calculate click errors
errs = click_locs - probe_locs

# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

cp.prep4ai()

# @@@ plot magnitude of the mislocalization across conditions
fig, ax = plt.subplots(1, figsize=(4, 4))
fig.suptitle(f"subID: {subID} – Rightward Motion - Fixed Probe Loc.")
ax.axhline(color='black')

ax.plot(-movobj_flash_pos,
        [errs[movobj_flash_pos_all == movobj_flash_pos[0]].mean()[0],
         errs[movobj_flash_pos_all == movobj_flash_pos[1]].mean()[0],
         errs[movobj_flash_pos_all == movobj_flash_pos[2]].mean()[0],
         errs[movobj_flash_pos_all == movobj_flash_pos[3]].mean()[0],
         errs[movobj_flash_pos_all == movobj_flash_pos[4]].mean()[0]], '-o')
ax.set(xlabel="Flash location wrt moving object's center [dva]",
       ylabel="Mislocalization in direction of motion [dva]")
ax.plot([-2.5, 2.5], [-.25, -.25], color='black', lw=3)

plt.savefig(os.path.join(save_dir, f"{subID}.pdf"))
