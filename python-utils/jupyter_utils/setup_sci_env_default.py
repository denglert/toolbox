import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import os
import scipy

# - Auto reload import libraries

get_ipython().magic('load_ext autoreload')
get_ipython().magic('autoreload 2')

import plot_utils.plot_utils as plu

# - Load in matplotline style file

home = os.path.expanduser("~")
mpl_style_dir = os.path.join(home, 'lib/prog/python/python-utils/mpl_style')
plt.style.use( os.path.join( mpl_style_dir, 'single_plot.mplstyle'))
#plt.style.use( os.path.join( mpl_style_dir, 'global.mplstyle'))

# - Pandas settings

pd.options.display.max_seq_items = 2000

# - Inline matplotlib figures

get_ipython().magic('matplotlib inline')
