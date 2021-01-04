.. raw:: html

    <style>
        table.docutils th, table.docutils td { white-space: normal }
    </style>

.. _infrastructure-python-packaging:

Python package installation in Aldryn Django projects
=====================================================

Python packages in Aldryn Django projects are installed using pip. Our :ref:`Dockerfile <dockerfile-reference>` for
Python projects performs three operations in sequence: it *compiles a list of dependencies*, *creates a list of
wheels*, and *installs the wheels*, using the following commands:

..  code-block:: Dockerfile

    RUN pip-reqs compile && \                   # compile a list of dependencies
        pip-reqs resolve && \                   # create a list of wheels
        pip install \                           # install the wheels
            --no-index --no-deps \              # ...disallows use of the index, prevents implicit installation of dependencies
            --requirement requirements.urls


Selective execution of commands
-------------------------------

By removing or commenting out the ``pip-reqs compile`` instruction after a successful compilation of all requirements,
you will prevent successive builds from reprocessing ``requirements.in``, pinning all the dependencies to exact
versions. This can be valuable, as upstream dependencies of dependencies may change at any time, and can cause a
failure on successive deployment - even if you haven't changed anything in the project yourself. See
:ref:`manage-dependencies` for more.

To isolate the behaviour and effects of any of these three commands, they can be run individually, for example::

  docker-compose run web pip-reqs compile

Alternatively, if you're not able to run commands in a container, comment out the ones you don't want to execute, and
try building with ``docker-compose build``.


Summary of commands
-------------------

.. list-table::
   :widths: auto

   * - *command*
     - ``pip-reqs compile``
     - ``pip-reqs resolve``
     - ``pip install``
   * - *input*
     - ``requirements.in``
     - ``requirements.txt``
     - ``requirements.urls``
   * - *action*
     - creates a complete dependency list
     - creates a list of wheels
     - installs the wheels
   * - *output*
     - ``requirements.txt``
     - ``requirements.urls``
     -
   * - *fails if*
     - a dependency cannot be found
     - a wheel cannot be found
     - pip is unable to install the wheel
   * - *typical cause*
     - :ref:`dependency conflict or no longer available <wheels-dependency-unfindable>`
     - :ref:`the wheels proxy was unable to build a wheel <wheels-dependency-unbuildable>`
     - :ref:`the wheel requires additional components for installation <wheels-dependency-uninstallable>`


Our wheels proxy
----------------

We maintain our own `DevPi server <https://github.com/devpi/devpi>`_ for private packages, and a
`Python wheels <https://pythonwheels.com/>`_ proxy.

Our wheels proxy creates wheels for all packages on `PyPI <https://pypi.org/>`_.

A `Python wheel <https://pythonwheels.com>`_ is a pre-compiled package, built for a particular platform (a combination
of the target operating system, architecture and Python version). Wheels offer numerous advantages over other Python
packaging options. On our platform, they reduce installation times significantly, both locally and on our
infrastructure. Using wheels also allows us to perform additional dependency resolution during installation.


Typical issues when installing wheels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will occasionally see an error in a deployment log that clearly refers to installation of Python packages,
occurring after the output::

  Step 7/9 : RUN pip-reqs compile &&
                 pip-reqs resolve &&
                 pip install --no-index --no-deps --requirement requirements.urls

This indicates that one of those commands has failed, usually in one of the following ways:


.. _wheels-dependency-unfindable:

A dependency cannot be found (from ``pip-reqs compile``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes a dependency cannot be found. This could be because a version has been specified incorrectly, or no longer
exists::

  Could not find a version that matches django==1.11.29,>2.0

Most commonly, it's because different packages in the same project either explicitly or implicitly specify conflicting
versions of a dependency (for example, ``django==1.11.29`` and ``django>2.0`` as above) at the same time. See
:ref:`debug-dependency-conflict` for more on this.


.. _wheels-dependency-unbuildable:

A wheel cannot be built (from ``pip-reqs resolve``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Occasionally, a wheel cannot be built for a particular package. This is usually because although the package exists on
PyPI, it is not compatible with the particular version of Python specified for that wheel (an example might be a Python
2 package in a Python 3 environment) and the attempt to build the wheel fails.

The error will appear in the logs as::

    HTTPError: 500 Server Error: Internal Server Error

from the wheels server. In such a case, check that the dependency mentioned is in fact suitable for the environment.


.. _wheels-dependency-uninstallable:

A wheel cannot be installed (from ``pip install``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, a wheel can be found and downloaded, but fails to install. Example output (in this case for
``jupyter``) might be::

  Installing build dependencies: started
  Installing build dependencies: finished with status 'error'
  ERROR: Complete output from command /usr/local/bin/python /usr/local/lib/python3.6/site-packages/pip install --ignore-installed --no-user --prefix /tmp/pip-build-env-2xou1hp2/overlay --no-warn-script-location --no-binary :none: --only-binary :none: --no-index -- setuptools wheel jupyter:
  ERROR: Collecting setuptools
  ERROR: Could not find a version that satisfies the requirement setuptools (from versions: none)
  ERROR: No matching distribution found for setuptools

In this case, the wheel was found and downloaded, but could not be installed because it contained a "hidden" dependency
(``setuptools``). One option is to contact Divio support; we can ensure that the wheel is built with this requirement.

Another is to bypass the wheels proxy, described in :ref:`wheels-not-using-proxy` below.


.. _wheels-not-using-proxy:

Not using the wheels proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~

You don't have to use our wheels proxy, though it's the default and it's strongly recommended. To change the way
Python installs packages, see the ``Dockerfile``.


Bypassing the proxy for a particular dependency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, you would remove the dependency from the ``requirements.in`` so that it is not processed by the default
installation commands; then, it would be added to the ``Dockerfile`` just before them, for example:

..  code-block:: Dockerfile

  RUN pip install jupyter==1.0.0


Bypassing the proxy altogether
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is not recommended, but the default installation commands can be replaced with:

..  code-block:: Dockerfile

    RUN pip install --requirement requirements.in

Our standard ``Dockerfile`` for Python/Django projects contains::

    ENV PIP_INDEX_URL=${PIP_INDEX_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/+simple/} \
        WHEELSPROXY_URL=${WHEELSPROXY_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/}

Removing this will use PyPI instead of our own PyPI server.

..  important::

    If you plan to deploy your changes in Divio's infrastructure, you will need to remove the ``# <PYTHON>`` comments to avoid the automatic population mechanism overwriting your changes as described here :ref:`how-the-dockerfile-is-automatically-populated`


Caching
-------

See :ref:`docker-layer-caching` for the implications of caching for package installation with pip.
