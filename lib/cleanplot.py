import numpy as np
import matplotlib as plt
from matplotlib.patches import Polygon


def remove_box(ax):
    # removes the upper and the right borders of the axis
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def prep4ai():
    plt.rcParams['pdf.fonttype'] = 42  # AI can detect text now
    plt.rcParams['font.sans-serif'] = "Arial"
    plt.rcParams['font.size'] = 8
