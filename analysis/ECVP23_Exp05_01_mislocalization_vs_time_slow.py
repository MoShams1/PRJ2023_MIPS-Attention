"""
Project MIPS-SProf
Mo Shams <MShamsCBR@gmail.com>
Initiated on: Feb 27, 2023
---

Analyzes data from ECVP23_Exp05
To show the magnitude of the mislocalization of a flashed object at
different times wrt a moving object's sweep at half speed

"""
import os
import numpy as np
import pandas as pd
from matplotlib import ticker
import matplotlib.pyplot as plt
from lib import cleanplot as cp
from matplotlib.patches import Polygon


# ----------------------------------------------------------------------------

# /// CONFIGURE PATHS AND LOAD DATA ///

data_dir = os.path.join('..', 'data', 'ECVP23_Exp05')
save_dir = os.path.join('..', 'result', 'ECVP23')
file_name = "AR1_20230227_200934.json"
subID = file_name[:3]
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
# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

# /// set plot parameters
cp.prep4ai()

# convert theta to time
times = (thetas - 90) / 90 * 500  # in ms
# --------------------------------------

fig, ax = plt.subplots(1, figsize=(4, 4))
fig.suptitle(f"subID: {subID} – Effect of sweep time")
ax.plot(times, err_arr_x)
ax.axhline(color='k', linestyle='--')
ax.axvline(color='k', linestyle='--')
ax.set(xlabel='Sweep time wrt flash time [ms]',
       ylabel='Mislocalization in direction of motion [dva]')
plt.tight_layout()
plt.savefig(os.path.join(save_dir,
                         f"ECVP23_Exp05_{subID}_misloc_vs_sweeptime.pdf"))
# --------------------------------------
