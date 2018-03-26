#!/usr/bin/env python

import pandas as pd
import numpy as np


def lambda1(sina, mH, mh=125.09, v=246):
    sina2 = sina*sina
    cosa2 = 1.0 - sina2
    lambda1 = (mh**2/(2.0*v**2))*cosa2 + (mH**2/(2.0*v**2))*sina2
    return lambda1


def lambda2(sina, mH, tanb, mh=125.09, v=246):
    vs = v/tanb
    sina2 = sina*sina
    cosa2 = 1.0 - sina2
    lambda2 = (mh**2/(2.0*vs**2))*sina2 + (mH**2/(2.0*vs**2))*cosa2
    return lambda2


def lambda3(sina, mH, tanb, mh=125.09, v=246):
    vs = v/tanb
    cosa = np.sqrt(1.0 - sina*sina)
    sin2a = 2.0*sina*sina
    lambda3 = (mH**2 - mh**2)*sin2a/(2.0 * v * vs)
    return lambda3


def gHhh(sina, tanb, mH, mh=125.09, v=246):
    vs = v/tanb
    cosa = np.sqrt(1.0-sina**2)
    gHhh = - (sina*cosa/vs*v)*(sina * v + cosa * vs)*(mh**2 + mH**2/2.0)
    return gHhh
