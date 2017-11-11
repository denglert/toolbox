#!/usr/bin/env python

import os
import sys
import stat
import shutil
import yaml
import glob
import time
import pandas as pd
import utils.utils as utils
from collections import OrderedDict

MG5_rootDir     = "/home/de3u14/lib/build/hep/MadGraph/MG5_aMC_v2_4_2"
MWTC_Calculator = "/scratch/de3u14/MWTC/tools/MWT_Calculator/MWT_Calculator"

def create_MG5_process_dir(model, process, dir):
    """
    create_MG5_process_dir(model, process, dir)
    Example:
    create_MG5_process_dir('MWT_MG', 'p p > z h', './samples/pp_zh_LO_MG5_242' )
    """

    # - MadGraph5 root directory
    if MG5_rootDir not in sys.path:
        sys.path.append( MG5_rootDir )
    
    # - Command line interface
    import madgraph.interface.master_interface as interface
    
    # - Logging - #
    import logging, logging.config
    import madgraph.interface.coloring_logging
    logging.config.fileConfig(os.path.join( MG5_rootDir, 'madgraph', 'interface', '.mg5_logging.conf'))
    logging.root.setLevel(logging.ERROR)
    logging.getLogger('madgraph').setLevel(logging.ERROR)
    logging.getLogger('madevent').setLevel(logging.ERROR)
    
    # - me5_configuration.txt
    me5_card_original_path = os.path.join('./mg5_cards/me5_configuration.txt')
    
    cmd_line = interface.MasterCmd()

    cmd_line.run_cmd('import {}'.format(model))
    cmd_line.run_cmd('generate {}'.format(process))
    cmd_line.run_cmd('output {}'.format(dir))
    me5_card_path = os.path.join( dir, './Cards/me5_configuration.txt'   )
    shutil.copy2( me5_card_original_path, me5_card_path )


def get_ME5_cmd_line( dir ):

    # - Add process bin/internal directory to sys.path
    sys.path.append(os.path.join( dir,'bin','internal'))
    
    # - Import madevent_interface module - #
    import madevent_interface  as ME
    
    # - Logging - #
    import logging, logging.config, coloring_logging
    logging.config.fileConfig(os.path.join( dir, 'bin', 'internal', 'me5_logging.conf'))
    logging.root.setLevel(logging.ERROR)
    logging.getLogger('madevent').setLevel(logging.ERROR)

    # - Remove RunWeb
    utils.silentrm( os.path.join( dir, 'RunWeb') )
    
    # - Get command line
    cmd_line = ME.MadEventCmd( me_dir=dir )

    return cmd_line


def get_run_card( run_card_path ):

    # - MadGraph5 root directory
    if MG5_rootDir not in sys.path:
        sys.path.append( MG5_rootDir )

    import madgraph.various.banner as banner_mod  # run_card
    run_card = banner_mod.RunCard(       run_card_path   ) 

    return run_card

def get_param_card( process_dir, param_card_path ):

    process_internal_dir = os.path.join( process_dir, 'bin','internal')

    # - MadGraph5 root directory
    if MG5_rootDir not in sys.path:
        sys.path.append( MG5_rootDir )

    # - MadGraph5 root directory
    if process_internal_dir not in sys.path:
        sys.path.append( process_internal_dir )

    import check_param_card as param_card_mod # param_card
    param_card = param_card_mod.ParamCard( param_card_path ) 

    return param_card

mwtc_data = OrderedDict(
        [
        ('mA'              , None),
        ('gt'              , None),
        ('PS'              , None),
        ('rs'              , None),
        ('mh'              , None),
        ('M1N'             , None),
        ('M2N'             , None),
        ('M1C'             , None),
        ('M2C'             , None),
        ('wh'              , None),
        ('w1N'             , None),
        ('w1C'             , None),
        ('w2N'             , None),
        ('w2C'             , None),
        ('xsec'            , None)
        ])

def get_mwtc_data( param_card ):

    mwtc_data['gt']  = param_card['tcinput'].param_dict[ (1,)  ].value
    mwtc_data['mA']  = param_card['tcinput'].param_dict[ (2,)  ].value
    mwtc_data['PS']  = param_card['tcinput'].param_dict[ (3,)  ].value
    mwtc_data['rs']  = param_card['tcinput'].param_dict[ (4,)  ].value
    mwtc_data['mh']  = param_card['tcinput'].param_dict[ (5,)  ].value
    
    mwtc_data['M1N'] = param_card['mass'].param_dict[ (50,)  ].value
    mwtc_data['M2N'] = param_card['mass'].param_dict[ (51,)  ].value
    mwtc_data['M1C'] = param_card['mass'].param_dict[ (52,)  ].value
    mwtc_data['M2C'] = param_card['mass'].param_dict[ (53,)  ].value
    
    mwtc_data['wh']  = param_card['decay'].param_dict[ (25,)  ].value
    mwtc_data['w1N'] = param_card['decay'].param_dict[ (50,)  ].value
    mwtc_data['w2N'] = param_card['decay'].param_dict[ (51,)  ].value
    mwtc_data['w1C'] = param_card['decay'].param_dict[ (52,)  ].value
    mwtc_data['w2C'] = param_card['decay'].param_dict[ (53,)  ].value

    return mwtc_data

def setup_run_card( run_card_path, run_config ):

    process_run_card = get_run_card( run_card_path )

    # - Set run_card parameters accordingly
    for key, value in run_config['settings'].iteritems():
        process_run_card[key] = value

    process_run_card.write( run_card_path )

def setup_param_card( param_card_path, model_config, df=None, index=None ):

    import check_param_card as param_card_mod # param_card
    param_card = param_card_mod.ParamCard( param_card_path ) 

    for par, opts in model_config['mg5_parameters'].iteritems():
        if not 'value' in opts:
            param_card[ opts['block'] ].param_dict[ (opts['lhaid'],)   ].value = df.loc[index,par]
        else:
            param_card[ opts['block'] ].param_dict[ (opts['lhaid'],)   ].value = opts['value']

    param_card.write( param_card_path )



#####################################################
def get_cross_section( process_dir, run_config_path ):
    pass

#####################################################
def generate_event_sample( tag, process_dir, run_config_path, output_dir, info_file_path, model_config_path=None, info_file_index=0 ):
    """
    generate_events_sample(tag, process_dir, run_config_path, output_dir, info_file_path, model_config_path=None, info_file_index=0 )
    - tag:               used to label the process
    - process_dir:       process directory which is needed to be run
    - run_config_path:   path to the run configuration
    - output_dir:        output directory where the .root files are stored
    - info_file_path:    path to an (existing) ASCII file in which the xsec values are stored
    - model_config_path: path to the model related configuration file
    - info_file_index:   row number of the info file from which the parameters are read in
    """

    import yaml
    import utils.utils as utils
    import pandas as pd
    import glob
    import time
    
    # - Display info

    print('Called generate_event_sample with:')
    print('process_dir:       {}'.format(process_dir) )
    print('run_config_path:   {}'.format(run_config_path) )
    print('output_dir:        {}'.format(output_dir) )
    print('model_config_path: {}'.format(model_config_path) )
    print('info_file_index:   {}'.format(info_file_index) )

    # - Paths
    
    process_param_card_path = os.path.join( process_dir, 'Cards/param_card.dat')
    process_run_card_path   = os.path.join( process_dir, 'Cards/run_card.dat')

    ### --- Run configuration --- ###

    with open( run_config_path ) as f:
    	run_config = yaml.safe_load(f)

    setup_run_card(process_run_card_path, run_config)

    ### --- Pythia & Delphes --- ###

    process_pythia_card_path  = os.path.join( process_dir, 'Cards/pythia_card.dat') 
    process_delphes_card_path = os.path.join( process_dir, 'Cards/delphes_card.dat')

    if run_config['settings']['pythia']:
        shutil.copy2 ( run_config['pythia_card_path'], process_pythia_card_path )
    else:
        utils.silentrm( process_pythia_card_path  )

    if run_config['settings']['delphes']:
        shutil.copy2 ( run_config['delphes_card_path'], process_delphes_card_path )
    else:
        utils.silentrm( process_delphes_card_path  )
    
    ### --- Model configuration --- ###

    if model_config_path:
        with open( model_config_path ) as f:
    	    model_config = yaml.safe_load(f)

    ### --- Load in/create info DataFrame --- ###

    if os.path.isfile( info_file_path ):
        df = pd.read_table(info_file_path, delim_whitespace=True)
    else:
        df = pd.DataFrame()

    # - Remove RunWeb
    utils.silentrm( os.path.join( process_dir, 'RunWeb') )

    # - Get madevent5 command line prompt
    madevent_prompt = get_ME5_cmd_line( process_dir )

    # - If there is not model_config_path provided proceed with default parameters provided in the
    # - parameter card
    if not model_config_path:
        full_tag = tag
    else:
    # - If there is a model_config_path provided set parameters accordingly
        setup_param_card( process_param_card_path, model_config, df, info_file_index )
        full_tag = "{}".format(tag)
        # - Use tag parameters to construct full tag
        if model_config['tag_parameters']:
            for par_tag in model_config['tag_parameters']:
                full_tag = full_tag + "_{}_{:.1f}".format( par_tag, df.loc[info_file_index,par_tag] )

    madevent_prompt.run_cmd( 'generate_events -f {}'.format(full_tag) )

    xsec = madevent_prompt.results.current['cross']

    df.loc[info_file_index,"xsec_{}".format(tag)] = xsec

    # - Moving essential files
    if run_config['settings']['delphes']:
        shutil.move( glob.glob( os.path.join(process_dir, 'Events', full_tag, '*delphes_events.root'))[0],
                  os.path.join( output_dir, '{}_sample.root'.format(tag) ) )

    shutil.move( glob.glob( os.path.join(process_dir, 'Events', full_tag, '*banner*' ) )[0],
                 os.path.join( output_dir,  '{}_banner.txt'.format(tag) ) )

    shutil.rmtree( os.path.join(process_dir, 'Events', full_tag) )
    shutil.rmtree( os.path.join(process_dir, 'HTML',   full_tag) )

    df.to_csv( info_file_path, sep=' ', float_format='%.3e', index=False)

#####################################################
def generate_event_sample_MWTC( tag, process_dir, run_config_path, output_dir, info_file_path ):
    """
    generate_events_sample(tag, process_dir, run_config_path, output_dir, info_file_path, model_config_path=None, info_file_index=0 )
    - tag:               used to label the process
    - process_dir:       process directory which is needed to be run
    - run_config_path:   path to the run configuration
    - output_dir:        output directory where the .root files are stored
    - info_file_path:    path to an (existing) ASCII file in which the xsec values are stored
    """

    
    # - Display info

    print('Called generate_event_sample with:')
    print('process_dir:       {}'.format(process_dir) )
    print('run_config_path:   {}'.format(run_config_path) )
    print('output_dir:        {}'.format(output_dir) )
    print('model_config_path: {}'.format(model_config_path) )
    print('info_file_index:   {}'.format(info_file_index) )

    # - Paths
    
    process_run_card_path   = os.path.join( process_dir, 'Cards/run_card.dat')

    ### --- Run configuration --- ###

    with open( run_config_path ) as f:
    	run_config = yaml.safe_load(f)

    setup_run_card(process_run_card_path, run_config)

    ### --- Pythia & Delphes --- ###

    process_pythia_card_path  = os.path.join( process_dir, 'Cards/pythia_card.dat') 
    process_delphes_card_path = os.path.join( process_dir, 'Cards/delphes_card.dat')

    if run_config['settings']['pythia']:
        shutil.copy2 ( run_config['pythia_card_path'], process_pythia_card_path )
    else:
        utils.silentrm( process_pythia_card_path  )

    if run_config['settings']['delphes']:
        shutil.copy2 ( run_config['delphes_card_path'], process_delphes_card_path )
    else:
        utils.silentrm( process_delphes_card_path  )
    
    ### --- Model configuration --- ###

    if model_config_path:
        with open( model_config_path ) as f:
    	    model_config = yaml.safe_load(f)

    ### --- Load in/create info DataFrame --- ###

    if os.path.isfile( info_file_path ):
        df = pd.read_table(info_file_path, delim_whitespace=True)
    else:
        df = pd.DataFrame()

    # - Remove RunWeb
    utils.silentrm( os.path.join( process_dir, 'RunWeb') )

    # - Get madevent5 command line prompt
    madevent_prompt = get_ME5_cmd_line( process_dir )

    os.system("{} {} {} {} {} {} > {}".format( MWT_Calculator, pt['gt'], pt['mA'], pt['PS'], pt['rs'], mh, param_card_path ) )

    full_tag = full_tag + "_{}_{:.1f}".format( par_tag, df.loc[info_file_index,par_tag] )

    madevent_prompt.run_cmd( 'generate_events -f {}'.format(full_tag) )

    xsec = madevent_prompt.results.current['cross']

    df.loc[info_file_index,"xsec_{}".format(tag)] = xsec

    # - Moving essential files
    if run_config['settings']['delphes']:
        shutil.move( glob.glob( os.path.join(process_dir, 'Events', full_tag, '*delphes_events.root'))[0],
                  os.path.join( output_dir, '{}_sample.root'.format(tag) ) )

    shutil.move( glob.glob( os.path.join(process_dir, 'Events', full_tag, '*banner*' ) )[0],
                 os.path.join( output_dir,  '{}_banner.txt'.format(tag) ) )

    shutil.rmtree( os.path.join(process_dir, 'Events', full_tag) )
    shutil.rmtree( os.path.join(process_dir, 'HTML',   full_tag) )

    df.to_csv( info_file_path, sep=' ', float_format='%.3e', index=False)
