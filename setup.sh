BASEDIR=$(dirname $(realpath "$BASH_SOURCE"))
export TOOLBOX_DIR=${BASEDIR}

### --- Export environment variables --- ###

# - Matplotlib styles directory
export ENV_MATPLOTLIB_STYLES_DIR=${TOOLBOX_DIR}/python/matplotlib/styles/

# - Jupyter setup scripts
export ENV_JUPYTER_SETUPS_DIR=${TOOLBOX_DIR}/python/jupyter/setups/

# - Python modules
export PYTHONPATH=${TOOLBOX_DIR}/python/modules/:$PYTHONPATH
