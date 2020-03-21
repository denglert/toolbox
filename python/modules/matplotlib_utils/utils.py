#!/usr/bin/env bash

import os
import matplotlib as mpl
import matplot.pyplot as plt
import matplotlib.dates sa mdates



def savefig(fig, path):
    """
    Saves a figure to a path in .png and .pdf formats

    Parameters
    ---------
    fig : matplotlib figure
        Figure to be saved

    path : str
        Path where the figure should be saved.
        The path should be without the file extension (.png, .pdf)
    """
    
    if os.path.isfile(path):
        os.remove(path)

    dir = os.path.dirname(path)
    filename = os.path.basename(path)
    basename, ext = os.path.splitext(filename)

    osutils.mkdir_p(dir)

    path_pdf = os.path.join(dir, basename+'.pdf')
    path_png = os.path.join(dir, basename+'.png')

    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def rotate_tick_labels(ax,
                       ticks = "xticks",
                       angle = 45):
    """
    Rotates the ticks on the x axis.

    Parameters
    ----------
    ax : mpl axis

    ticks : str
        xticks or yticks

    angle : float
        Angle by which to rotate
    """

    if ticks == "xticks":
        ticklabels = ax.get_xticklabels()
    elif ticks == "yticks":
        ticklabels = ax.get_yticklabels()
    else:
        raise NameError("Unknown ticks {}".format(ticks))

    for tick in ticklabels:
        tick.set_rotation(angle)


def set_major_locator(axis,
                      major_locator
                      ):

    if major_locator == "year":
        axis.set_major_locator(mdates.YearLocator())
        axis.set_major_formatter(mdates.DateFormatter("%Y"))
    elif major_locator == "month":
        axis.set_major_locator(mdates.MonthLocator())
        axis.set_major_formatter(mdates.DateFormatter("%m/%y"))
    elif major_locator == "day":
        axis.set_major_locator(mdates.DayLocator())
        axis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    elif major_locator == "hour":
        axis.set_major_locator(mdates.HourLocator())
        axis.set_major_formatter(mdates.DateFormatter("%H"))




