import pandas as pd
import numpy as np
import glob
import os
from scipy.interpolate import interp1d

def init_ana_dict(ana_dict, channel, type):

    if not 'channels' in ana_dict:
        ana_dict['channels'] = {}

    if not channel in ana_dict['channels']:
        ana_dict['channels'][channel] = { } 
    if not type in ana_dict['channels'][channel]:
        ana_dict['channels'][channel][type] = {}

    return ana_dict

def print_nested_dict_keys(d):
    for k, v in d.items():
        if isinstance(v, dict):
            print("{0}".format(k))
            print_nested_dict_keys(v)
        else:
            print("{0}".format(k))


def get_analysis_bounds( path_to_folder ):

    paths = glob.glob( path_to_folder + "*.dat" )

    analysis = {}

    for path in paths:

        base     = os.path.basename(path)
        filename = os.path.splitext(base)[0]
        channel, limit_type = filename.split( '-' )

        df = pd.read_csv(path, delim_whitespace=True, names=['mass', 'upper_limit'])

        analysis = init_ana_dict(analysis, channel, limit_type)

        interpolated_func              = interp1d( df['mass'], df['upper_limit'])
        interpolated_func.bounds_error = False

        mass_min = df['mass'].min()
        mass_max = df['mass'].max()

        mass                = np.linspace( mass_min, mass_max, num=1000, endpoint=True)
        interpolated_values = interpolated_func(mass)

        to_be_stored = {'pts' : df,
                        'interpolated_func'  : interpolated_func,
                        'interpolated_values' : interpolated_values,
                        'mass' : mass}

        analysis['channels'][channel][limit_type] = to_be_stored

    return analysis


def apply_limits( df, analysis, mass ):

    for ch, ana_ch_dict in analysis['channels'].items():
        for type, ana_ch_type_dict in ana_ch_dict.items():

            col = analysis['name'] + '_' + ch + '_' + type
            df[col] = ana_ch_type_dict['interpolated_func']( df[mass] )

    for xsec_exp, xsec_model in analysis['compare'].items():
        col = xsec_exp + '_excl'
        df[col] = np.where( df[xsec_model] >  df[xsec_exp]*analysis['factor'],  True, False )
