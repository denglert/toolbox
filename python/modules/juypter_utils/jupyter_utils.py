#!/usr/bin/env python

# - https://github.com/jupyter/notebook/issues/1000


import json
import os.path
import re
import ipykernel
import requests

try:  # Python 3
    from urllib.parse import urljoin
except ImportError:  # Python 2
    from urlparse import urljoin

try:  # Python 3
    from notebook.notebookapp import list_running_servers
except ImportError:  # Python 2
    import warnings
    from IPython.utils.shimmodule import ShimWarning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ShimWarning)
        from IPython.html.notebookapp import list_running_servers


def get_notebook_name():
    """
    Return the full path of the jupyter notebook.
    """
    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return os.path.join(ss['notebook_dir'], relative_path)




# - Needs further dev to be able to overwrite output file
def save_notebook_to_html(out_html_path=None):

    notebook_path = get_current_notebook_path()
    cmd = 'jupyter nbconvert --to html {notebook}'.format(notebook=notebook_path)
    print("Running os command:\n{}.".format(cmd))
    os_signal = os.system(cmd)

    html_created_inplace_path = notebook_path.replace('ipynb', 'html')
    html_created_inplace_name = os.path.basename(html_created_inplace_path)

    if out_html_path is not None:
        if os.path.isdir(out_html_path):
            out_html_path = os.path.join(out_html_path, html_created_inplace_name)
        shutil.move(html_created_inplace_path, out_html_path)
    else:
        out_html_path = html_created_inplace
    
    msg = "{} should be created".format(out_html_path)
    print(msg)

    return os_signal == 0

