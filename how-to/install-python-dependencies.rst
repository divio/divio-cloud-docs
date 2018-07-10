.. _install-python-dependencies:

How to add arbitrary Python dependencies to a project
=====================================================

..  seealso::

    * :ref:`tutorial-add-applications`
    * :ref:`Add new applications to a project tutorial <install-system-packages>`


Your Divio Cloud project has a ``requirements.in`` file, processed by the
``pip-compile`` command from `pip-tools
<https://github.com/jazzband/pip-tools>`_.

Place your dependencies in the file, making sure that they are *outside* the::

    # <INSTALLED_ADDONS>...

    # </INSTALLED_ADDONS>

tags, since that part of the file is maintained automatically and is overwritten automatically with
the requirements from the Addons system.

.. _pinning-dependencies:

..  admonition:: Wherever possible, **pin your dependencies**

    An unpinned dependency is a hostage to fortune, and is highly likely to break something
    without warning when a new release is made.

    Unpinned dependencies are the **number one cause of deployment failures**. Nothing in the
    codebase may have changed, but a fresh deployment can unexpectedly pick up a newly-released
    version of a package.

    Sometimes your dependencies may themselves have unpinned dependencies. In this case, it
    can be worth explicitly pinning those too.

    When `installing from a version control repository <pip-install-from-online-package>`_, it is
    strongly recommended to pin the package by specifying a tag or commit, rather than  branch.


Installing from PyPI
--------------------

Use the package name, pinned with an optional (but :ref:`very strongly recommended
<pinning-dependencies>`) version number, for example::

    markdown=2.6.8


.. _pip-install-from-online-package:

Installing from an online package or version control system
-----------------------------------------------------------

You can use the URL of a tarballed or zipped archive of the package, typically provided by a
version control system.


Examples from GitHub
~~~~~~~~~~~~~~~~~~~~

Master branch, as tarball::

    https://github.com/account/repository/archive/master.tar.gz

or as a zipped archive::

    https://github.com/account/repository/archive/master.zip

Specify a different branch::

    https://github.com/account/repository/archive/develop.zip

However, we :ref:`very strongly recommend <pinning-dependencies>` specifying either a tag::

    https://github.com/account/repository/archive/1.6.0.zip

or a commit::

    https://github.com/account/repository/archive/2d8197e2ec4d01d714dc68810997aeef65e81bc1.zip

.. _vcs-protocol-support:

..  note::

    Our ``pip`` set-up does **not** support `VCS protocols
    <https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support>`_,

    However, as long as the version control system host offers full package downloads, you can use
    the tarball or zip archive URL for that to install from the VCS.


Rebuild the Docker container
----------------------------

To rebuild the Docker container, installing the new dependencies::

    docker-compose build web
