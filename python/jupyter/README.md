# Jupyter setup scripts

To load the setup scripts, inside the jupyter notebook run the following:

~~~~
import os
setup_script = os.path.join(os.environ['ENV_JUPYTER_SETUPS_DIR'], 'setup_sci_env_basic.py')
%run $setup_script
~~~~
