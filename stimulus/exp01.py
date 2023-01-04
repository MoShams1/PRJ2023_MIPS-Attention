"""
Project MIPS-Anisotropy
Mo Shams <MoShamsCBR@gmail.com> Jan 03, 2023

In this experiment, my aim is to map the mislocalization of single flashed
probe in the vicinity of a moving object in high resolution.
"""

# ----------------------------------------------------------------------------

# /// SESSION META DATA ///

subID = 'test'
N_BLOCKS = 1
N_TRIALS = 2
screen_num = 0  # 0: primary    1: secondary
refresh_rate = 120
full_screen = True
# ----------------------------------------------------------------------------

# /// CONFIGURE VISUAL OBJECTS ///

# /// fixation dot (function: add_fixdot)
fixdot_size
fixdot_pos
fixdot_color

# /// flashing object(s) (function: add_flash)
flashobj_size
flashobj_pos
flashobj1_color
flashobj2_color

# /// moving object (function: add_movobj; will call gen_path function)
movobj_size
movobj_dir
movobj_path
movobj_color

# ///





