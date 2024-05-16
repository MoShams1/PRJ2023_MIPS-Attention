"""
***** Project PRJ2023_MIPS-Attention
***** Experiment 01

        Mo Shams <MShamsCBR@gmail.com>
        Jan 06, 2023

To show the spatial profile of the mislocalization of a flashed object in
the vicinity of a moving object.

"""
import os
import numpy as np
import pandas as pd
from matplotlib import ticker
import matplotlib.pyplot as plt
from lib import cleanplot as cp
from matplotlib.patches import Polygon


# ----------------------------------------------------------------------------

# /// FUNCTIONS ///

def modify_maps(ax, contour=False, contour_im=None):
    vertices = np.array([(0 - 2.5, 5 - 2.5),
                         (0 + 2.5, 5 - 2.5),
                         (0 + 2.5, 5 + 2.5),
                         (0 - 2.5, 5 + 2.5)])
    poly = Polygon(vertices, fc='none', ec='black', lw=2)
    ax.add_patch(poly)
    ax.plot(0, 0, '+', markersize=15, color='black')
    cp.trim_spines(ax)
    if contour:
        for c in contour_im.collections:
            c.set_edgecolor("face")


def limit_large(ax):
    ax.set(xlim=[-7, 10], ylim=[-4, 13])


def limit_small(ax):
    ax.set(xlim=[-5, 8], ylim=[-1.5, 11.5])


def modify_upper_ax(ax):
    ax.set(xlim=[-5, 8])
    cp.trim_spines(ax)


def modify_side_ax(ax):
    ax.set(ylim=[-1.5, 11.5])
    cp.trim_spines(ax)


def clean_colormap(ax):
    xticks = ticker.MaxNLocator(min_n_ticks=3, nbins=5)
    ax.xaxis.set_major_locator(xticks)


# ----------------------------------------------------------------------------

# /// CONFIGURE PATHS AND LOAD DATA ///

data_dir = os.path.join('..', 'data', 'raw', 'exp01')
save_dir = os.path.join('..', 'result', 'exp01')
file_name = "MS1_20230106_154600.json"
subID = file_name[:3]
file_address = os.path.join(data_dir, file_name)
df = pd.read_json(file_address)
# ----------------------------------------------------------------------------

# /// CONFIGURE DATA ///

# /// flip the data in leftward codition
msk_rightdir = df['movobj_dir'] == 1
msk_leftdir = df['movobj_dir'] == -1

click_locs = df.click_loc.apply(pd.Series)
probe_locs = df.probe_loc.apply(pd.Series)

click_locs.loc[msk_leftdir, 0] = -click_locs.loc[msk_leftdir, 0]
probe_locs.loc[msk_leftdir, 0] = -probe_locs.loc[msk_leftdir, 0]

# /// calculate click errors
errs = click_locs - probe_locs

# /// create the error arrays
k = 81
probe_arr_x = np.full(k, fill_value=np.nan)
probe_arr_y = np.full(k, fill_value=np.nan)
err_arr_x = np.full(k, fill_value=np.nan)
err_arr_y = np.full(k, fill_value=np.nan)
probe_xs = probe_locs[0]
probe_xs = np.unique(probe_xs)
probe_xs.sort()
probe_ys = probe_locs[1]
probe_ys = np.unique(probe_ys)
probe_ys.sort()
probe_ys = probe_ys[::-1]
pcnt = -1
for probe_x in probe_xs:
    for probe_y in probe_ys:
        pcnt += 1
        ind_loc = (probe_locs[0] == probe_x) & (probe_locs[1] == probe_y)
        probe_arr_x[pcnt] = np.mean(probe_locs[ind_loc], axis=0)[0]
        probe_arr_y[pcnt] = np.mean(probe_locs[ind_loc], axis=0)[1]
        err_arr_x[pcnt] = np.mean(errs[ind_loc], axis=0)[0]
        err_arr_y[pcnt] = np.mean(errs[ind_loc], axis=0)[1]

# /// create the error maps
k = (9, 9)
probe_map_x = np.full(k, fill_value=np.nan)
probe_map_y = np.full(k, fill_value=np.nan)
herr_map = np.full(k, fill_value=np.nan)
verr_map = np.full(k, fill_value=np.nan)
for i, probe_x in enumerate(probe_xs):
    for j, probe_y in enumerate(probe_ys):
        ind_loc = (probe_locs[0] == probe_x) & (probe_locs[1] == probe_y)
        probe_map_x[j, i] = np.mean(probe_locs[ind_loc], axis=0)[0]
        probe_map_y[j, i] = np.mean(probe_locs[ind_loc], axis=0)[1]
        herr_map[j, i] = np.mean(errs[ind_loc], axis=0)[0]
        verr_map[j, i] = -np.mean(errs[ind_loc], axis=0)[1]

# /// calculate mislocalization along each axis
# horizontal error along x axis (>0: towards motion)
herr_x = np.mean(herr_map, 0)
# horizontal error along y axis (>0: towards motion)
herr_y = np.mean(herr_map, 1)
# vertical error along x axis (>0: towards fixation)
verr_x = np.mean(verr_map, 0)
# vertical error along y axis (>0: towards fixation)
verr_y = np.mean(verr_map, 1)
# ----------------------------------------------------------------------------

# @@@ PLOT RESULTS @@@

# /// set plot parameters
cp.prep4ai()
ncontours = 100
# --------------------------------------

# @@@ map of probes and clicks
fig, axs = plt.subplots(1, 2, figsize=(8, 4))
fig.suptitle(f"subID: {subID} – Probes, Clicks, and Error Map")
axs[0].plot(click_locs[0], click_locs[1],
            '.', color='grey')
axs[0].plot(probe_locs[0], probe_locs[1],
            'o', mec='red', mfc='none')
axs[0].set(xlabel='Horizontal position wrt fixation [deg]',
           ylabel='Vertical position wrt fixation [deg]')
limit_large(axs[0])
modify_maps(axs[0])

axs[1].quiver(probe_arr_x, probe_arr_y,
              err_arr_x, err_arr_y,
              color='grey', width=0.004)
axs[1].set(xlabel='Horizontal position wrt fixation [deg]',
           ylabel='Vertical position wrt fixation [deg]')
limit_large(axs[1])
modify_maps(axs[1])

plt.savefig(os.path.join(save_dir, f"{subID}_probes_clicks_errors.pdf"))
# --------------------------------------

# @@@ horizontal mislocalization map
fig, axs = plt.subplots(3, 2, figsize=(5.5, 6),
                        gridspec_kw={'width_ratios': [4, 1],
                                     'height_ratios': [1, 4, .5]})
fig.suptitle(f"subID: {subID} – Horizontal Misloc. Map")
im = axs[1, 0].contourf(probe_map_x, probe_map_y, herr_map,
                        levels=ncontours, cmap='viridis')
limit_small(axs[1, 0])
modify_maps(axs[1, 0])
cbar_ax = axs[1, 0].inset_axes([0, -.2, 1, .02])
fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
clean_colormap(cbar_ax)
axs[1, 0].set(xlabel='Horizontal position wrt fixation [deg]',
              ylabel='Vertical position wrt fixation [deg]')
limit_small(axs[1, 0])
modify_maps(axs[1, 0], contour=True, contour_im=im)

axs[0, 0].plot(probe_xs, herr_x, color='black')
axs[0, 0].set(ylabel='Misloc. towards fixation [deg]')
modify_upper_ax(axs[0, 0])

axs[1, 1].plot(herr_y, probe_ys, color='black')
axs[1, 1].set(xlabel='Misloc. towards fixation [deg]')
modify_side_ax(axs[1, 1])

axs[0, 1].axis('off')
axs[2, 0].axis('off')
axs[2, 1].axis('off')

plt.savefig(os.path.join(save_dir, f"{subID}_horizontal_err_map.pdf"))
# --------------------------------------

# @@@ vertical mislocalization map
fig, axs = plt.subplots(3, 2, figsize=(5.5, 6),
                        gridspec_kw={'width_ratios': [4, 1],
                                     'height_ratios': [1, 4, .5]})
fig.suptitle(f"subID: {subID} – Vertical Misloc. Map")
im = axs[1, 0].contourf(probe_map_x, probe_map_y, verr_map,
                        levels=ncontours, cmap='viridis')
limit_small(axs[1, 0])
modify_maps(axs[1, 0])
cbar_ax = axs[1, 0].inset_axes([0, -.2, 1, .02])
fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
clean_colormap(cbar_ax)
axs[1, 0].set(xlabel='Horizontal position wrt fixation [deg]',
              ylabel='Vertical position wrt fixation [deg]')
limit_small(axs[1, 0])
modify_maps(axs[1, 0], contour=True, contour_im=im)

axs[0, 0].plot(probe_xs, verr_x, color='black')
axs[0, 0].set(ylabel='Misloc. towards fixation [deg]')
modify_upper_ax(axs[0, 0])

axs[1, 1].plot(verr_y, probe_ys, color='black')
axs[1, 1].set(xlabel='Misloc. towards fixation [deg]')
modify_side_ax(axs[1, 1])

axs[0, 1].axis('off')
axs[2, 0].axis('off')
axs[2, 1].axis('off')

plt.savefig(os.path.join(save_dir, f"{subID}_vertical_err_map.pdf"))
# --------------------------------------
