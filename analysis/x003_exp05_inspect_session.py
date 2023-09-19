"""
***** Project MIPS-Attention
***** Experiment 05

        Mo Shams <MShamsCBR@gmail.com>
        Jan 18, 2023

To inspect each session of experiment 5, where a moving object either
reverses at its midway or continues in its original direction.

"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lib import cleanplot as cp


# ----------------------------------------------------------------------------

# /// FUNCTIONS ///
def modify_bars(ax):
    ax.axhline(color='black')
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', length=0)
    cp.trim_spines(ax)


# ----------------------------------------------------------------------------

# /// CONFIGURE PATHS AND LOAD DATA ///

data_dir = os.path.join('..', 'data', 'raw', 'exp05')
save_dir = os.path.join('..', 'result', 'exp05')
file_name = "MS1_20230119_152802_blocked.json"
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
msk_trail = probe_locs[0] < 0
msk_lead = probe_locs[0] > 0

# /// extract erros in each condition
errs_tr_pas = errs[msk_trail & msk_passed][0]
errs_ld_pas = errs[msk_lead & msk_passed][0]
errs_tr_rev = errs[msk_trail & msk_reversed][0]
errs_ld_rev = errs[msk_lead & msk_reversed][0]
# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

cp.prep4ai()

# @@@ plot magnitude of the mislocalization across conditions
fig, axs = plt.subplots(1, 2, figsize=(4, 4), sharey=True)
fig.suptitle(f"subID: {subID} – Blocked order")
axs[0].bar([1, 2], [np.mean(errs_tr_pas), np.mean(errs_ld_pas)], color='grey')
axs[0].plot(1*np.ones(errs_tr_pas.size), errs_tr_pas,
            'o', mec='k', mfc='none')
axs[0].plot(2*np.ones(errs_ld_pas.size), errs_ld_pas,
            'o', mec='k', mfc='none')
axs[0].set(xticks=[1, 2], xticklabels=['trailing probe', 'leading probe'],
           ylabel='Horiz. misloc. wrt motion  dir. [deg]',
           title='Passing trajectory')
modify_bars(axs[0])

axs[1].bar([1, 2], [np.mean(errs_tr_rev), np.mean(errs_ld_rev)], color='grey')
axs[1].plot(1*np.ones(errs_tr_rev.size), errs_tr_rev,
            'o', mec='k', mfc='none')
axs[1].plot(2*np.ones(errs_ld_rev.size), errs_ld_rev,
            'o', mec='k', mfc='none')
axs[1].set(xticks=[1, 2], xticklabels=['trailing probe', 'leading probe'],
           title='Reversive trajectory')
modify_bars(axs[1])
plt.tight_layout()

plt.savefig(os.path.join(save_dir, f"{subID}_blocked_order.pdf"))
