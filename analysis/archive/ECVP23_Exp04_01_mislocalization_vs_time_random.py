"""
Project PRJ2023_MIPS-Attention
Mo Shams <MShamsCBR@gmail.com>
Initiated on: Feb 27, 2023
---

Analyzes data from ECVP23_Exp04
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

# ----------------------------------------------------------------------------

# /// CONFIGURE PATHS AND LOAD DATA ///

data_dir = os.path.join('..', 'data', 'ECVP23_Exp04')
save_dir = os.path.join('..', 'result', 'ECVP23')
file_name = "AR01_20230227_200155.json"
# file_name = "MS01_20230228_115928.json"
# file_name = "0001_20230601_113509.json"
# file_name = "0005_20230602_110336.json"
# file_name = "0011_20230601_121629.json"
# file_name = "1191_20230602_114506.json"
# file_name = "2002_20230601_110153.json"
subID = file_name[:4]
file_address = os.path.join(data_dir, file_name)
df = pd.read_json(file_address)
# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

# /// set plot parameters
cp.prep4ai()

# convert theta to time
times = (thetas - 90) / 360 * 1000  # in ms
# --------------------------------------

fig, ax = plt.subplots(1, figsize=(4, 4))
fig.suptitle(f"subID: {subID} – Effect of sweep time - random")
ax.plot(times, err_arr_x)
ax.axhline(color='k', linestyle='--')
ax.axvline(color='k', linestyle='--')
ax.set(xlabel='Sweep time wrt flash time [ms]',
       ylabel='Mislocalization in direction of motion [dva]')
plt.tight_layout()
plt.savefig(os.path.join(save_dir,
                         f"ECVP23_Exp04_{subID}_misloc_vs_sweeptime.pdf"))
# --------------------------------------
