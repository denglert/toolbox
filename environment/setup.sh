# - Note:
# - When sourcing this script the current working directory should be the root directory of the toolbox

TOOLBOX_DIR=$(pwd)

### --- Export environment variables --- ###

# - Matplotlib styles directory
export ENV_MATPLOTLIB_STYLES_DIR=${TOOLBOX_DIR}/python/matplotlib/styles/

# - Jupyter setup scripts
export ENV_JUPYTER_SETUPS_DIR=${TOOLBOX_DIR}/python/jupyter/setups/

# - Python modules
export PYTHONPATH=${TOOLBOX_DIR}/python/modules/:$PYTHONPATH
