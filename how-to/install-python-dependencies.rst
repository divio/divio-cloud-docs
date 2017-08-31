.. _install-python-dependencies:

How to add arbitrary Python dependencies to a project
=====================================================

..  note:: See also: :ref:`install-system-packages`

Your Divio Cloud project has a ``requirements.in`` file, processed by the
``pip-compile`` command from `pip-tools
<https://github.com/jazzband/pip-tools>`_.

Place your dependencies in the file, making sure that they are *outside* the::

    # <INSTALLED_ADDONS>...

    # </INSTALLED_ADDONS>

tags, since that part of the file is maintained automatically and is overwritten automatically with the requirements
from the Addons system.

Installing from PyPI
--------------------

Use the package name, with an optional (but recommended) version number, for
example::

    markdown=2.6.8


Installing from version control
-------------------------------

You can use a version control system URL, such as::

    https://github.com/some_account/some_repository/archive/master.tar.gz

..  note::

    In this case you need to use the *tarball URL*, as in the example, rather than the URL you'd use for cloning.


Rebuild the Docker container
----------------------------

To rebuild the Docker container, installing the new dependencies::

    docker-compose build web
