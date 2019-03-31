#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

ENV_MATPLOTLIB_STYLES_DIR = os.environ['ENV_MATPLOTLIB_STYLES_DIR']

font0 = FontProperties()

def load_mpl_style(style_file):
    style_file_fullpath = os.path.join(ENV_MATPLOTLIB_STYLES_DIR, style_file)
    plt.style.use(style_file_fullpath)
