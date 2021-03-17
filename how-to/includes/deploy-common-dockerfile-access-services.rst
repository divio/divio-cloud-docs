Access to environment and services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  warning::

    During the build process, Docker has no access to to the application's environment or services.

    This means you cannot run database operations such as database migrations during the build process. Instead, these
    should be handled later as :ref:`release commands <release-commands>`.
