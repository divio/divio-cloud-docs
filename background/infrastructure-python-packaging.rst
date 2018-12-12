.. _infrastructure-python-packaging:

Python packaging on Divio Cloud
===============================

Python packages in Divio Cloud projects are installed using pip.

The appropriate section in the :ref:`Dockerfile <dockerfile-reference>` processes the project's
``requirements.in`` (or, if you have :ref:`pinned all dependencies <manage-dependencies>`, its
``requirements.in``).

We maintain our own `DevPi server <https://github.com/devpi/devpi>`_ for private packages, and a
`Python wheels <https://pythonwheels.com/>`_ proxy.

Our wheels proxy creates wheels for all packages on `PyPI <https://pypi.org/>`_.

Using wheels reduces installation times significantly, because the process does not need to compile
binaries - it can instead download our platform-specific binaries.

Using wheels also allows us to perform additional dependency resolution during installation.
