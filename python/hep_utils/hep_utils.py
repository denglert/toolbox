import pandas as pd
import numpy as np
import glob
import os
from scipy.interpolate import interp1d

def analysis_template():
    """Returns a blank analysis template (dictionary)."""

    analysis = {}

    analysis['limits']      = {'exp' : None, 'obs': None }
    analysis['description'] = None
    analysis['plot_label']  = None
    analysis['factor']      = None
    analysis['compare']     = None

    return analysis


def import_limits_to_analysis( analysis, limitfile_path, limit_type='exp' ):
    """Import the limit information into an analysis object."""

    # - Read in .dat file into a pd.DataFrame()
    df = pd.read_csv(limitfile_path, delim_whitespace=True, names=['mass', 'limit'])

    # - Interpolated the limit points
    interpolated_func              = interp1d( df['mass'], df['limit'])
    interpolated_func.bounds_error = False

    # - Get minimum and maximum masses
    mass_min = df['mass'].min()
    mass_max = df['mass'].max()

    # - Create a dense sample of the interpolated function (for plotting purposes later)
    mass                = np.linspace( mass_min, mass_max, num=1000, endpoint=True)
    interpolated_values = interpolated_func(mass)

    # - Dictionary which is to be stored in 
    limit_info = { 'pts' : df,
                   'interpolated_func'   : interpolated_func,
                   'interpolated_pts' : interpolated_values,
                   'mass_pts' : mass }

    # - Pass the stored values to the analysis
    analysis['limits'][limit_type] = limit_info





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


def tag_excluded_points(df, analysis):

    if not analysis['limits']['exp'] == None:
        tag_excluded_points_limit_type(df, analysis, type='exp')

    if not analysis['limits']['obs'] == None:
        tag_excluded_points_limit_type(df, analysis, type='obs')


def tag_excluded_points_limit_type( df, analysis, type='exp' ):
    """Tag each parameter points whether it is excluded by an analysis or not.
       Creates two new columns:
        - 'analysis['name']_<type>': analysis cross section value at the mass.
        - 'analysis['compare'].key()_excl' """

    ## - Add analysis cross-section corresponding to the mass pts
    # - Column name
    col_name  = analysis['name'] + '_' + type

    # - Mass label
    mass_label = analysis['mass_label']

    # - Limit information 
    limit_info = analysis['limits'][type]

    # - Add column with the corresponding analysis cross section
    df[col_name] = limit_info['interpolated_func']( df[mass_label] )

    # - Add a column storing boolean values indicating whether parameter point is excluded or not 
    for xsec_exp, xsec_theory in analysis['compare'].items():

        # - Column name
        col_name = xsec_exp + '_excl'

        # - Add a new column storing whether the pt is excluded or not.
        df[col_name] = np.where( df[xsec_theory] >  df[xsec_exp]*analysis['factor'],  True, False )
