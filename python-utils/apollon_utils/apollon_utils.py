#!/usr/bin/env python

import os
import sys
import stat
import shutil
import subprocess

def launch_apollon( prog, workdir, comp_config, bin_config, nEvents ):

    apollon_bin_dir = '/home/de3u14/lib/projects/Apollon/bin/'
    cmd = [ os.path.join(apollon_bin_dir, prog), workdir, comp_config, bin_config, str(nEvents) ] 
    print('cmd: ', cmd)

    #process = subprocess.Popen( cmd, stdout=subprocess.PIPE)
    #process.wait()

    subprocess.call( cmd )


def create_component_config( path, xsec, lumi ):

    config_path = os.path.join( path, 'apollon.conf' )

    config = \
    """# Tag name
tag test

# Number of components
nComp 4

# Name of the components
compname0 gg_zh1_all
compname1 gg_zh1_SM_only
compname2 gg_zh1_A_only
compname3 qq_zh1

# Cross section (fb) of each component
compxsec0 {0}
compxsec1 {1}
compxsec2 {2}
compxsec3 579.5

isSmear yes

# Number of generated events for each component
compnev0 10000

# Component color
# Colors:
# 0 - white, 1 - black, 2 - red, 3 - green, 4 - blue, 5 - yellow
compcolor0 2

GlobalTextLabel Benchmark_B1_22.66fb
GlobalTextPosX  0.55
GlobalTextPosY  0.85
GlobalTextSize  0.025

# Components Paths
comppath0 {3}/sample/gg_Zh_all.root
comppath1 {3}/sample/gg_Zh_SM_only.root
comppath2 {3}/sample/gg_Zh_A_only.root
comppath3 /scratch/de3u14/2HDM-Zh/MadGraph/samples/2HDMtII/2HDMtII_NLO_qq_Zh1_LO_with_b_quark_MG5_242/Events/2HDM_tII_SM_limit_sinbma_1.00/tag_1_delphes_events.root

# Luminosity (fb-1)
lumi {4}
    """.format( xsec[0], xsec[1], xsec[2], path, lumi )
    

    # - Write job scripts
    with open( config_path , 'w') as f:
        f.write( config )
    

###########################################################

def create_component_config_SM( path, xsec, lumi ):

    config_path = os.path.join( path, 'apollon.conf' )

    config = \
    """# Tag name
tag test

# Number of components
nComp 2

# Name of the components
compname0 gg_Zh
compname1 qq_Zh

# Cross section (fb) of each component
compxsec0 {0}
compxsec1 {1}

isSmear yes

# Number of generated events for each component
compnev0 100000

# Component color
# Colors:
# 0 - white, 1 - black, 2 - red, 3 - green, 4 - blue, 5 - yellow
compcolor0 2

GlobalTextLabel -
GlobalTextPosX  0.55
GlobalTextPosY  0.85
GlobalTextSize  0.025

# Components Paths
comppath0 {2}/sample/gg_Zh_all.root
comppath1 {2}/sample/qq_Zh_ud_quarks_only.root

# Luminosity (fb-1)
lumi {3}
    """.format( xsec[0], xsec[1], path, lumi )
    
    # - Write job scripts
    with open( config_path , 'w') as f:
        f.write( config )

#################################################################
def create_component_config( work_dir, tag, model_config, info_file_path, info_file_index = 0 ):

    import pandas as pd

    df = pd.read_table( info_file_path, delim_whitespace=True )

    nComponents = len(model_config['components'])

    config_path = os.path.join( work_dir, 'apollon', 'apollon.conf' )
    sample_dir  = os.path.join( work_dir, 'samples' )

    config_str = \
    """# Tag name
isSmear yes

# Luminosity (fb-1)
lumi {0}

# Number of components
nComp {1}
    """.format( model_config['luminosity'], nComponents ) 

    for iComp, component in enumerate(model_config['components'] ):
        
        comp_xsec = df.loc[info_file_index, 'xsec_{}'.format(component) ]
        comp_path = os.path.join(sample_dir, "{}_sample.root".format( component) )
        comp_name = component

        config_str = config_str + "\ncompname{0} {1}".format( iComp, comp_name )
        config_str = config_str + "\ncompxsec{0} {1}".format( iComp, comp_xsec )
        config_str = config_str + "\ncomppath{0} {1}".format( iComp, comp_path )

    # - Write job scripts
    with open( config_path , 'w') as f:
        f.write( config_str )

#################################################################
def create_component_config_mod( work_dir, tag, model_config, info_file_path, info_file_index = 0 ):

    import pandas as pd
    import glob

    df = pd.read_table( info_file_path, delim_whitespace=True )

    nComponents = len(model_config['components'])

    config_path = os.path.join( work_dir, 'apollon', 'apollon.conf' )
    sample_dir  = os.path.join( work_dir, 'samples' )

    config_str = \
    """# Tag name
isSmear yes

# Luminosity (fb-1)
lumi {0}

# Number of components
nComp {1}
    """.format( model_config['luminosity'], nComponents ) 

    for iComp, component in enumerate(model_config['components'] ):
        
        comp_xsec = df.loc[info_file_index, 'xsec_{}'.format(component) ]
        comp_path = os.path.join(sample_dir, "{}_{}_sample.root".format(component, tag) )
        comp_name = component

        config_str = config_str + "\ncompname{0} {1}".format( iComp, comp_name )
        config_str = config_str + "\ncompxsec{0} {1}".format( iComp, comp_xsec )
        config_str = config_str + "\ncomppath{0} {1}".format( iComp, comp_path )

    # - Write job scripts
    with open( config_path , 'w') as f:
        f.write( config_str )
