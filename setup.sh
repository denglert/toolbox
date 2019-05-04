# - Get the absolute path of the dir where the this setup script is residing.
# - Should be compatible with both linux & mac.
BASEDIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export TOOLBOX_DIR=${BASEDIR}

echo "TOOLBOX_DIR=${TOOLBOX_DIR}"

### --- Export environment variables --- ###

# - Matplotlib styles directory
export ENV_MATPLOTLIB_STYLES_DIR=${TOOLBOX_DIR}/python/matplotlib/styles/

# - Jupyter setup scripts
export ENV_JUPYTER_SETUPS_DIR=${TOOLBOX_DIR}/python/jupyter/setups/

# - Python modules
export PYTHONPATH=${TOOLBOX_DIR}/python/modules/:$PYTHONPATH
