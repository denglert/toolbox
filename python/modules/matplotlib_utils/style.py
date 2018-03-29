#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font0 = FontProperties()


def text_ATLAS(a, x_pos, y_pos, label="ATLAS", style="italic", fontweight="bold", fontsize=16,
        coordinate='axes'):

    if coordinate == 'axes':
        transform = a.transAxes
    elif coordinate == 'data':
        transform = a.transData

    a.text(x_pos, y_pos, label, style=style, fontweight=fontweight, fontsize=fontsize,
            transform=transform)

def text_ATLAS_label(a, x_pos, y_pos, fontsize=20, x_shift=0.25, version_text="Internal", coordinate='axes'):

    text_ATLAS(a, x_pos, y_pos, fontsize=fontsize, coordinate=coordinate)
    
    if coordinate == 'axes':
        transform = a.transAxes
    elif coordinate == 'data':
        transform = a.transData

    a.text(x_pos+x_shift, y_pos, version_text, fontsize=fontsize, transform=transform)


def text_collider_setup(a, x_pos, y_pos, sqrt_s='13 TeV', lumi='36.1fb', coordinate='axes'):

    collider_setup_text = r"$\sqrt{{s}} =$ {}, {}".format(sqrt_s, lumi)
    if coordinate == 'axes':
        transform = a.transAxes
    elif coordinate == 'data':
        transform = a.transData

    a.text(x_pos, y_pos, collider_setup_text, transform=transform)


def text_ATLAS_full_info(a, x_pos, y_pos, version_x_shift=0.11, collider_x_shift=0.00,
        collider_y_shift=-0.06, version_text="Internal",
        sqrt_s='13 TeV', lumi='36.1 fb', fontsize=14, coordinate='axes'):

    text_ATLAS_label(a, x_pos, y_pos, fontsize=fontsize, x_shift=version_x_shift, coordinate=coordinate)
    text_collider_setup(a, x_pos+collider_x_shift, y_pos+collider_y_shift, sqrt_s, lumi, coordinate=coordinate)
