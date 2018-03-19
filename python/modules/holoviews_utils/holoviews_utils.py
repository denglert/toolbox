#!/usr/bin/env python

import holoviews as hv
import numpy as np
from matplotlib.mlab import griddata

hv.extension('bokeh')

def make_hv_Image(x,y,z, nxSpaces=101, nySpaces=101):
    """Creates a hv.Image"""
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    xs = np.linspace(x.min(), x.max(), nxSpaces)
    ys = np.linspace(y.min(), y.max(), nySpaces)
    xi,yi = np.meshgrid(xs,ys)
    z = griddata(x, y, z, xi, yi, interp='linear')
    img = hv.Image((xs, ys, z), bounds=(x_min,y_min,x_max,y_max))
    return img


def url_hook(url, plot, element):
    taptool = TapTool(callback=OpenURL(url=url))
    plot.state.tools.append(taptool)


def disable_logo(plot, element):
    plot.state.toolbar.logo = None
    hv.plotting.bokeh.ElementPlot.finalize_hooks.append(disable_logo)
