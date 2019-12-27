.. _project-anatomy:

Anatomy of a Divio project
================================

A Divio project is contained in a Git repository. The files in the repository are used to build the project image, from
which its containers are instantiated.


``Dockerfile``
--------------

The key file is the ``Dockerfile`` that defines the project.


Local development files
------------------------

Some files are only present, or only used, when in the local development environment.


``.aldryn``
~~~~~~~~~~~

Added to the local project by the ``divio project setup`` command, to provide an identifier for the
corresponding cloud project. Not part of the repository.


``.env-local``
~~~~~~~~~~~~~~

On the cloud, environment variables can be set via the Control Panel. Locally, they can be supplied
in ``.env-local``. This is part of the repository, so it is recommended not to commit sensitive
configuration values.


``docker-compose.yml``
~~~~~~~~~~~~~~~~~~~~~~

The :ref:`docker-compose.yml file <docker-compose-yml-reference>` describes the Docker configuration of the local
environment, and the services compose the whole Docker application. It's part of the repository, but is ignored on
the cloud.


``data``
~~~~~~~~

For local development use only. In ``data``, a ``media`` directory functions as the local analogue
of Cloud project's S3 storage bucket (see :ref:`interact-storage`).


Aldryn Addons directories
--------------------------

Not all projects use the Aldryn Addons system. Those that do will contain:


``addons``
~~~~~~~~~~

For each addon in your project, a directory will be created in ``addons``, containing:

* ``addon.json``: basic metadata for the addon (generally, there is no need ever to edit this file)
* ``aldryn_config.py``: optional; manages settings for the addon (see :ref:`aldryn_config.py
  explanation <aldryn-config>` and :ref:`how to create an aldryn_config.py file
  <create-aldryn-config>`)
* ``settings.json``: any settings that were applied via the Control Panel, so that they can
  be used locally


``addons-dev``
~~~~~~~~~~~~~~

For local development use only. An addon can be placed here for development purposes.
``addons-dev`` contains a little magic; any packages within directories in ``addons-dev`` will
automatically be placed on the Python path for convenience.

Running ``divio project develop <addon>`` for an addon in ``addons-dev`` will add it to the
project's ``requirements.in`` and ``settings.INSTALLED_ADDONS``, then attempt to build the
project.
