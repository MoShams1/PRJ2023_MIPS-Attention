import numpy as np


def linear(pos1, pos2, dur):
    pathx = np.linspace(pos1[0], pos2[0], dur)
    pathy = np.linspace(pos1[1], pos2[1], dur)
    return pathx, pathy
