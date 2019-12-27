.. _infrastructure-python-packaging:

Python packaging on Divio
===============================

Python packages in Divio projects are installed using pip.

The appropriate section in the :ref:`Dockerfile <dockerfile-reference>` processes the project's
``requirements.in`` (or, if you have :ref:`pinned all dependencies <manage-dependencies>`, its
``requirements.txt``).


Our wheels proxy
----------------

We maintain our own `DevPi server <https://github.com/devpi/devpi>`_ for private packages, and a
`Python wheels <https://pythonwheels.com/>`_ proxy.

Our wheels proxy creates wheels for all packages on `PyPI <https://pypi.org/>`_.

A `Python wheel <https://pythonwheels.com>`_ is a pre-compiled packaged, built for a particular platform. Wheels offer
numerous advantages over other Python packaging options.

Using wheels reduces installation times significantly, both locally and on our infrastructure. Using wheels also allows
us to perform additional dependency resolution during installation.


Not using the wheels proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~

You don't have to use our wheels proxy, though it's the default and it's strongly recommended. To change the way
Python installs packages, see the ``Dockerfile``. Our standard ``Dockerfile`` for Python/Django projects contains::

    ENV PIP_INDEX_URL=${PIP_INDEX_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/+simple/} \
        WHEELSPROXY_URL=${WHEELSPROXY_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/}

This can be removed or changed, along with the subsequent instruction::

    RUN pip install --requirement requirements.in


Caching
-------

See :ref:`docker-layer-caching` for the implications of caching for package installation with pip.
