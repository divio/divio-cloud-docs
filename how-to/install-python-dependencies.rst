.. _install-python-dependencies:

How to install Python dependencies in a project
===============================================

..  seealso::

    * :ref:`Adding applications to a project <tutorial-add-applications>` in our tutorial
    * :ref:`How to install system packages <install-system-packages>`

To install dependencies in a project, you must first :ref:`list-dependencies`, then
:ref:`process-dependencies`. Both steps are described below.

.. _list-dependencies:

List your dependencies
----------------------

Your Divio Cloud project has a ``requirements.in`` file, processed by the ``pip-compile`` command
from `pip-tools <https://github.com/jazzband/pip-tools>`_ when the project is built.

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

    When :ref:`installing from a version control repository <pip-install-from-online-package>`, it
    is strongly recommended to pin the package by specifying a tag or commit, rather than branch.

    Sometimes your dependencies may themselves have unpinned dependencies. In this case, it
    can be worth explicitly pinning those too - you can easily :ref:`pin all dependencies in a
    project <manage-dependencies>` automatically.


Listing packages from PyPI
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the package name, pinned with an optional (but :ref:`very strongly recommended
<pinning-dependencies>`) version number, for example::

    markdown==2.6.8


.. _pip-install-from-online-package:

Listing packages from version control systems or as archives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the URL of a tarballed or zipped archive of the package, typically provided by a
version control system.

..  important::

    More recent versions of `pip tools <https://pypi.org/project/pip-tools/>`_ as used in the Divio base projects
    require you to use URLS that provide the ``egg`` fragment (as shown in the examples below), and will raise an error
    if they encounter URLs lacking it. Older versions would allow you to omit the fragment.


Examples from GitHub
^^^^^^^^^^^^^^^^^^^^

Master branch, as tarball::

    https://github.com/account/repository/archive/master.tar.gz#egg=package-name

or as a zipped archive::

    https://github.com/account/repository/archive/master.zip#egg=package-name

Specify a different branch::

    https://github.com/account/repository/archive/develop.zip#egg=package-name

However, we :ref:`very strongly recommend <pinning-dependencies>` specifying either a tag::

    https://github.com/account/repository/archive/1.6.0.zip#egg=package-name

or a commit::

    https://github.com/account/repository/archive/2d8197e2ec4d01d714dc68810997aeef65e81bc1.zip#egg=package-name

.. _vcs-protocol-support:

..  note::

    Our ``pip`` set-up does **not** support `VCS protocols
    <https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support>`_ - you cannot use for
    example URLs starting ``git+`` or ``hg+``, such as ``git+git@github.com:divio/django-cms.git``.

    However, as long as the version control system host offers full package downloads, you can use
    the tarball or zip archive URL for that to install from the VCS, as in the examples above.


.. _process-dependencies:

Process the list
----------------

The requirements file is processed when the project is build. This is taken care of in Cloud
deployments by the :ref:`Dockerfile <dockerfile-reference-python>`, and locally by running a
``build`` command::

    docker-compose build web

Make sure that you don't also have a ``requirements.txt`` of pinned dependencies, otherwise you
will simply be re-installing the old list.
