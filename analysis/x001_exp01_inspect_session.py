"""
Project MIPS-Anisotropy – Analysis – Experiment 01
Mo Shams <MShamsCBR@gmail.com> Jan 06, 2023

To show the spatial profile of the mislocalization of a flashed object in
the vicinity of a moving object.

"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ----------------------------------------------------------------------------

# /// LOAD DATA ///

data_dir = os.path.join('..', 'data', 'raw')
file_name = "MS1_20230106_154600.json"
file_address = os.path.join(data_dir, file_name)
df = pd.read_json(file_address)
# ----------------------------------------------------------------------------

# /// CONFIGURE DATA ///

# /// flip the data in leftward codition
msk_rightdir = df['motion_dir'] == 1
msk_leftdir = df['motion_dir'] == -1

click_locs = df.click_loc.apply(pd.Series)
probe_locs = df.probe_loc.apply(pd.Series)

click_locs.loc[msk_leftdir, 0] = -click_locs.loc[msk_leftdir, 0]
probe_locs.loc[msk_leftdir, 0] = -probe_locs.loc[msk_leftdir, 0]

# /// calculate click errors
errs = click_locs - probe_locs

# /// create the map
# find unique x and y positions of the probe
k = 9
err_map_x = np.full((k, k), fill_value=np.nan)
err_map_y = np.full((k, k), fill_value=np.nan)
probe_xs = probe_locs[0]
probe_xs = np.unique(probe_xs)
probe_xs.sort()
probe_ys = probe_locs[1]
probe_ys = np.unique(probe_ys)
probe_ys.sort()
probe_ys = probe_ys[::-1]
for i, probe_x in enumerate(probe_xs):
    for j, probe_y in enumerate(probe_ys):
        ind_loc = (probe_locs[0] == probe_x) & (probe_locs[1] == probe_y)
        err_map_x[j, i] = np.mean(errs[ind_loc], axis=0)[0]
        err_map_y[j, i] = np.mean(errs[ind_loc], axis=0)[1]

# /// calculate mislocalization along each axis
# horizontal error along x axis
herr_x = np.mean(err_map_x, 0)
# horizontal error along y axis
herr_y = np.mean(err_map_x, 1)
# vertical error along x axis
verr_x = np.mean(err_map_y, 0)
# vertical error along y axis
verr_y = np.mean(err_map_y, 1)
# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

# @@@ map of probes and clicks
_, axs = plt.subplots(1, figsize=(7, 4))
axs.plot(click_locs[0], click_locs[1],
         '.', color='black')
axs.plot(probe_locs[0], probe_locs[1],
         'o', mec='red', mfc='none')
axs.set(xlim=[-12, 12], ylim=[-3, 12])
vertices = np.array([(0 - 2.5, 5 - 2.5),
                     (0 + 2.5, 5 - 2.5),
                     (0 + 2.5, 5 + 2.5),
                     (0 - 2.5, 5 + 2.5)])
poly = Polygon(vertices, facecolor='none', edgecolor='black', alpha=.5)
axs.add_patch(poly)

# @@@ mislocalization map
fig, axs = plt.subplots(1, figsize=(5, 5))
im = axs.imshow(err_map_x, cmap='copper', vmin=-2.5, vmax=2.5)
fig.colorbar(im, ax=axs)

# @@@ mislocalization along each axis
_, axs = plt.subplots(2, 2, figsize=(7, 7))
axs[0, 0].plot(herr_x)
axs[0, 1].plot(herr_y)
axs[1, 0].plot(verr_x)
axs[1, 1].plot(verr_y)

