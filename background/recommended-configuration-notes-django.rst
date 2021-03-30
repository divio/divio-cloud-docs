.. _working-with-recommended-django-configuration:

Working with our recommended Django project configuration
=============================================================

Our recommended Django project configuration is described in:

* :ref:`deploy-django`
* :ref:`quickstart-django`
* :ref:`django-cms-deploy-quickstart`

The Twelve-factor model adopted for these projects places all configuration in environment variables, so that the project can
readily be moved to another host or platform, or set up locally for development. The configuration for:

* security
* database
* media
* static files

settings is handled by a few simple code snippets in ``settings.py``. In each case, the settings will fall back to
safe and secure defaults.


Application container
------------------------

In both local and cloud environments, the application will run in a ``web`` container, using the same image and
exactly the same codebase.


Django server
------------------

In cloud environments: the ``Dockerfile`` contains a ``CMD`` that starts up Django using the production application
gateway server.

In the local environment: the ``command`` line in ``docker-compose.yml`` starts up Django using the runserver,
overriding the ``CMD`` in the ``Dockerfile``. If the ``command`` line is commented out, ``docker-compose up`` will use
the application gateway server locally instead.


Database
------------

In cloud environments: the application will use one of our database clusters.

In the local environment: the application will use a container running the same database.

During the build phase: the database falls back to in-memory SQLite, as there is no database available to connect to,
and no configuration variables available from the environment in any case.


Security settings
------------------

Debug mode
~~~~~~~~~~~~

In cloud environments: the application will safely fall back to ``DEBUG = False``.

In the local environment: ``.env-local`` supplies a ``DJANGO_DEBUG`` variable to allow Django to run in debug mode.


Secret key
~~~~~~~~~~~~

In cloud environments: a random ``SECRET_KEY`` variable is always provided and will be used.

In the local environment: where no ``SECRET_KEY`` environment variable is provided, the application will fall back to a
hard-coded key in ``settings.py``.


Allowed hosts
~~~~~~~~~~~~~~~~~~

In cloud environments: ``DOMAIN`` and ``DOMAIN_ALIASES`` variable are always provided and will be used.

In the local environment: default values are provided via the ``DOMAIN_ALIASES`` environment variable in ``.env-local``.


Static files
------------

In cloud environments: the application gateway server and WhiteNoise are used.

In the local environment: static files are served by the Django runserver. When you instead run the application gateway
server locally and enforce ``DEBUG = False``, it can be tested with WhiteNoise in the local environment.


Media files
------------

In cloud environments: file storage and serving is handled by the S3 instance.

In the local environment: the local filesystem is used for storage, and Django's runserver is used to serve media. If a
cloud environment's ``DEFAULT_STORAGE_DSN`` is applied in the ``.env-local`` file, the local server will use the S3
instance instead.


Database migrations
------------------------

In its current state, database migrations are not executed automatically in cloud deployments. To run migrations
automatically, add a :ref:`release command <release-commands>`: ``python manage.py migrate``. Alternatively you can run
the command manually in the cloud environment using SSH.
