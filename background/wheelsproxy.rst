.. raw:: html

    <style>
        table.docutils th, table.docutils td { white-space: normal }
    </style>


.. _wheels-proxy:

Python wheels proxy
=======================

We maintain our own `DevPi server <https://github.com/devpi/devpi>`_ for private packages, and a
`Python wheels <https://pythonwheels.com/>`_ proxy as a convenience for our Python users.


Python wheels
-------------

When a Python package is installed from source, the installer must be able to install required components. This can
include compilation of system-level libraries, and can in turn require the presence of particular compilers, system
libraries and so on in order to succeed. Compiling some packages can take many minutes, slowing down deployments
and the development process.

Python wheels are a solution to this problem. A `Python wheel <https://pythonwheels.com>`_ is a pre-compiled package,
built for a particular platform (a combination of the target operating system, architecture and Python version). Wheels
offer numerous advantages over other Python packaging options. On our platform, they reduce installation times
significantly, both locally and on our infrastructure. Using wheels also allows us to perform additional dependency
resolution during installation.

An increasing number of Python packages are now distributed as wheels, making installation swifter and more reliable.
If a package is available as a wheel, pip and other installers will make use of it.

Not all packages are compiled as wheels however, and not all are compiled for the Python version and host architecture
that a particular application uses. In these cases, the installer will attempt to install from source.

Our wheels proxy server ensures that Python projects always have wheels available for their dependencies. It mirrors
`PyPI <https://pypi.org/>`_ and automatically builds wheels for every single package, targeting our server architecture
and several supported versions of Python for each.

Using our wheels proxy is optional, but allows packages to be installed - and Docker images to be built - much faster
(it also reduces the load on our build servers).

Aldryn projects :ref:`use our wheels proxy by default <wheels-proxy-aldryn>`. Currently we only support the use
of the wheels proxy in Aldryn projects.


.. _wheels-proxy-aldryn:

The wheels proxy in Aldryn Django projects
------------------------------------------------------

Our ``Dockerfile`` for Aldryn projects contains:

..  code-block:: Dockerfile

    ENV PIP_INDEX_URL=${PIP_INDEX_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/+simple/} \
        WHEELSPROXY_URL=${WHEELSPROXY_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/}

This makes use of an environment variable ``WHEELS_PLATFORM`` set in the build environment by the base image (see `an
example for our Python 3.9 image running in Debian Slim Buster
<https://github.com/divio/ac-base/blob/master/py3.9-slim-buster/Dockerfile#L95>`_. In turn, the values it sets for
``PIP_INDEX_URL`` and ``WHEELSPROXY_URL`` are used by ``pip-reqs``.

``pip-reqs`` first compiles a list of dependencies, then resolves that to a list of wheel URLs, which are then installed
with ``pip``:

..  code-block:: Dockerfile

    RUN pip-reqs compile && \                   # compile a list of dependencies
        pip-reqs resolve && \                   # create a list of wheels
        pip install \                           # install the wheels
            --no-index --no-deps \              # ...disallows use of the index, prevents implicit installation of dependencies
            --requirement requirements.urls


Summary of commands
~~~~~~~~~~~~~~~~~~~~

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


Typical issues when installing wheels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will occasionally see an error in a deployment log that clearly refers to installation of Python packages,
occurring after the output::

  Step 7/9 : RUN pip-reqs compile &&
                 pip-reqs resolve &&
                 pip install --no-index --no-deps --requirement requirements.urls

This indicates that one of those commands has failed, usually in one of the following ways:


.. _bad-request-for-url:

Bad request for URL (from from ``pip-reqs resolve``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A malformed Pip URL will raise a ``Bad Request for url`` error, for example:

..  code-block:: text

    Error: Bad Request for url: https://wheels.aldryn.net/v1/aldryn-extras+pypi/aldryn-baseproject-v4-py36/+resolve/

This is often caused by a URL that omits the required version number in the ``egg`` fragment, or is otherwise malformed.

See :ref:`pip-install-from-online-package` for more details and examples of how to use Pip URLs.


.. _wheels-dependency-unfindable:

A dependency cannot be found (from ``pip-reqs compile``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes a dependency cannot be found. This could be because a version has been specified incorrectly, or no longer
exists:

..  code-block:: text

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

The error will appear in the logs as:

..  code-block:: text

    HTTPError: 500 Server Error: Internal Server Error

from the wheels server. In such a case, check that the dependency mentioned is in fact suitable for the environment.


.. _wheels-dependency-uninstallable:

A wheel cannot be installed (from ``pip install``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, a wheel can be found and downloaded, but fails to install. Example output (in this case for
``jupyter``) might be:

..  code-block:: text

    Installing build dependencies: started
    Installing build dependencies: finished with status 'error'
    ERROR: Complete output from command /usr/local/bin/python /usr/local/lib/python3.6/site-packages/pip install --ignore-installed --no-user --prefix /tmp/pip-build-env-2xou1hp2/overlay --no-warn-script-location --no-binary :none: --only-binary :none: --no-index -- setuptools wheel jupyter:
    ERROR: Collecting setuptools
    ERROR: Could not find a version that satisfies the requirement setuptools (from versions: none)
    ERROR: No matching distribution found for setuptools

In this case, the wheel was found and downloaded, but could not be installed because it contained a "hidden" dependency
(``setuptools``). One option is to contact Divio support; we can ensure that the wheel is built with this requirement.
