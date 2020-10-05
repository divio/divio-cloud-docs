Divio environment variables
===========================

Divio cloud environments are automatically provided with a number of environment variables that can be used to
configure the applications that run in them. These can also be overridden in the *Environment variables* view in
the Control Panel.

.. _env-var-database-dsn:


``DATABASE_URL``, ``<prefix>_DATABASE_DSN``
  Each database provisioned in :ref:`Services <services>` will have a corresponding environment variable, for example
  ``DEFAULT_DATABASE_DSN`` (depending on the prefix applied - the default prefix is always ``DEFAULT``). The
  ``DEFAULT_DATABASE_DSN`` is also exposed as ``DATABASE_URL``

.. _env-var-domain:

``DOMAIN``
    The primary domain of the environment's server.

.. _env-var-domain-aliases:

``DOMAIN_ALIASES``
    Other domains for the environment, separated by commas.

.. _env-var-git-branch:

``GIT_BRANCH``
    The cloud environment's Git branch.

.. _env-var-secret-key:

``SECRET_KEY``
    A generated random key that your application can use as a unique identifier for internal security purposes.

.. _env-var-stage:

``STAGE``
  The name of the environment (``test``, ``live``, etc).

.. _env-var-storage-dsn:

``<prefix>_STORAGE_DSN``
  Each object storage provisioned in :ref:`Services <services>` will have a corresponding environment variable, for
  example ``DEFAULT_STORAGE_DSN`` (depending on the prefix applied - the default prefix is always ``DEFAULT``).
