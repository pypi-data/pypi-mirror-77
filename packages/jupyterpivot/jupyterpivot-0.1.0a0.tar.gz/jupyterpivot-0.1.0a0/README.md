jupyterpivot
===============================

pivottable.js for jupyter

Installation
------------

To install use pip:

    $ pip install jupyterpivot
    $ jupyter nbextension enable --py --sys-prefix jupyterpivot

To install for jupyterlab

    $ jupyter labextension install jupyterpivot

For a development installation (requires npm),

    $ git clone https://github.com/seadev.org/jupyterpivot.git
    $ cd jupyterpivot
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix jupyterpivot
    $ jupyter nbextension enable --py --sys-prefix jupyterpivot
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.

