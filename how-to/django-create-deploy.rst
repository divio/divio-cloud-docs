..  _django-create-deploy:

.. meta::
   :description:
       This guide explains step-by-step how to create and deploy a Twelve-factor Django project including Postgre or
       MySQL, and cloud media storage using S3, with Docker.
   :keywords: Docker, Django, Postgres, MySQL, S3


How to create and deploy a Django project
===========================================================================================

This guide will take you through the steps to: create a `Twelve-factor <https://www.12factor.net/config>`_ Django project, including:

* Postgres or MySQL database
* cloud media storage using S3
* `WhiteNoise <http://whitenoise.evans.io>`_ to serve static files in production
* `uWSGI <https://uwsgi-docs.readthedocs.io>`_, `Gunicorn <https://docs.gunicorn.org>`_ or `Uvicorn
  <https://www.uvicorn.org>`_ for the application gateway server

and to deploy it using Docker.

This guide assumes that you are familiar with the basics of the Divio platform and have Docker and the Divio CLI
installed. If not, please start with :ref:`our complete tutorial for Django <introduction>`.


Create a blank Divio project
----------------------------

Create a new project, selecting the *No Platform* > *Empty* options. In the newly-created project, use the *Services*
menu to add a Postgres or MySQL database, and an S3 object storage instance for media. Use the options menu to
provision each service.


Build the project locally
--------------------------

Run ``setup``
~~~~~~~~~~~~~

Run:

..  code-block:: bash

    divio project setup <project-slug>


The ``Dockerfile``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Edit the ``Dockerfile``, adding:

..  code-block:: Dockerfile

    FROM python:3.8
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt


..  _django-create-deploy-requirements:

Python requirements in ``requirements.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Dockerfile`` expects to find a ``requirements.txt`` file, so add one, containing:

..  code-block:: Dockerfile
    :emphasize-lines: 7-9, 11-14

    django>=3.1,<3.2
    dj-database-url==0.5.0
    django-storage-url==0.5.0
    whitenoise==5.2.0
    boto3==1.14.49

    # Select one of the following for the database
    psycopg2==2.8.5
    mysqlclient==2.0.1

    # Select one of the following for the gateway server
    uwsgi==2.0.19.1
    uvicorn==0.11.8
    gunicorn==20.0.4


Local container orchestration with ``docker-compose.yml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need this in order to be able to run the application locally for development purposes. Create a
``docker-compose.yml`` file, :ref:`for local development purposes <docker-compose-local>`. This will replicate the
``web`` image used in cloud deployments, and will set up:

* a Postgres or MySQL database running in a local container (instead of on a cloud database cluster)
* local file storage (instead of S3 instance)

..  code-block:: yaml
    :emphasize-lines: 17-19, 23-43

    version: "2.4"
    services:
      web:
        # the application's web service (container) will use an image based on our Dockerfile
        build: "."
        # map the internal port 80 to port 8000 on the host
        ports:
          - "8000:80"
        # map the host directory to app (which allows us to see and edit files inside the container)
        volumes:
          - ".:/app:rw"
          - "./data:/data:rw"
        # the default command to run wheneve the container is launched
        command: python manage.py runserver 0.0.0.0:80
        # the URL 'postgres' or 'mysql' will point to the application's db service
        links:
          # select one of the following for the database
          - "db:postgres"
          - "db:mysql"
        env_file: .env-local

      db:
        # Select one of the following db configurations for the database
        image: postgres:9.6-alpine
        environment:
          POSTGRES_DB: "db"
          POSTGRES_HOST_AUTH_METHOD: "trust"
        volumes:
          - ".:/app:rw"

        image: mysql:5.7
        environment:
          MYSQL_DATABASE: "db"
          MYSQL_ALLOW_EMPTY_PASSWORD: "yes"
          SERVICE_MANAGER: "fsm-mysql"
        volumes:
          - ".:/app:rw"
          - "./data/db:/var/lib/mysql"
        healthcheck:
            test: "/usr/bin/mysql --user=root -h 127.0.0.1 --execute \"SHOW DATABASES;\""
            interval: 2s
            timeout: 20s
            retries: 10


Local configuration using ``.env-local``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you can see above, the ``web`` service refers to an ``env_file`` containing the environment variables that will be
used in the local development environment. Create a ``.env-local`` file, containing:

..  code-block:: text
    :emphasize-lines: 1-3

    # select one of the following for the database
    DEFAULT_DATABASE_DSN=postgres://postgres@postgres:5432/db
    DEFAULT_DATABASE_DSN=mysql://root@mysql:3306/db

    DEFAULT_STORAGE_DSN=file:///data/media/?url=%2Fmedia%2F
    DJANGO_DEBUG=True
    DOMAIN_ALIASES=localhost, 127.0.0.1


Build with Docker
~~~~~~~~~~~~~~~~~

Now you can build the application containers locally:

..  code-block:: bash

    docker-compose build


Create the Django project module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application can be run inside its container now and commands can be executed in the Docker environment. Use it to create a new Django project module:

..  code-block:: bash

    docker-compose run web django-admin startproject myapp .

If you use a different name, you will need to change the reference to ``myapp`` in the :ref:`static settings <django-create-deploy-static>` and the ``Dockerfile``'s ``CMD`` line,
:ref:`below <django-create-deploy-CMD>`.


Configure ``settings.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit ``myapp.settings.py``, to add some code that will read configuration from environment variables, instead of hard-coding it. Add some imports:

..  code-block:: python

    import os
    import dj_database_url
    from django_storage_url import dsn_configured_storage_class


Some security-related settings - the cloud environments will provide these values where appropriate, and they will fall
back to safe values otherwise:

..  code-block:: python

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get('SECRET_KEY', '<a string of random characters>')

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = os.environ.get('DJANGO_DEBUG') == "True"

    DIVIO_DOMAIN = os.environ.get('DOMAIN', '')
    DIVIO_DOMAIN_ALIASES = [
        d.strip()
        for d in os.environ.get('DOMAIN_ALIASES', '').split(',')
        if d.strip()
    ]
    ALLOWED_HOSTS = [DIVIO_DOMAIN] + DIVIO_DOMAIN_ALIASES


Configure database settings:

..  code-block:: python

    # Configure database using DEFAULT_DATABASE_DSN; fall back to sqlite in memory when no
    # environment variable is available, e.g. during Docker build
    DEFAULT_DATABASE_DSN = os.environ.get('DEFAULT_DATABASE_DSN', 'sqlite://:memory:')

    DATABASES = {'default': dj_database_url.parse(DEFAULT_DATABASE_DSN)}


..  _django-create-deploy-static:

Configure static and media settings. First, add the ``WhiteNoiseMiddleware`` to the list of ``MIDDLEWARE``, after the
``SecurityMiddleware``:

..  code-block:: python
    :emphasize-lines: 3

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        [...]
    ]

and then:

..  code-block:: python

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Media files
    # DEFAULT_FILE_STORAGE is configured using DEFAULT_STORAGE_DSN

    # read the setting value from the environment variable
    DEFAULT_STORAGE_DSN = os.environ.get('DEFAULT_STORAGE_DSN')

    # dsn_configured_storage_class() requires the name of the setting
    DefaultStorageClass = dsn_configured_storage_class('DEFAULT_STORAGE_DSN')

    # Django's DEFAULT_FILE_STORAGE requires the class name
    DEFAULT_FILE_STORAGE = 'myapp.settings.DefaultStorageClass'

    # only required for local file storage and serving, in development
    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join('/data/media/')

(Note that the ``DEFAULT_FILE_STORAGE`` assumes your Django project was named ``myapp``.)


..  _django-create-deploy-CMD:

Extend the ``Dockerfile``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that a Django project has been created, append to a command to the ``Dockerfile`` that will collect static files.
Depending which application gateway server :ref:`you installed above <django-create-deploy-requirements>`, include the
appropriate command to launch the application when a container starts:

..  code-block:: Dockerfile
    :emphasize-lines: 3-6

    RUN python manage.py collectstatic --noinput

    # Select one of the following application gateway server commands
    CMD uwsgi --http=0.0.0.0:80 --module=myapp.wsgi
    CMD gunicorn --bind=0.0.0.0:80 myapp.wsgi
    CMD uvicorn --host=0.0.0.0 --port=80 myapp.asgi:application

(Note that this assumes your Django project was named ``myapp``.)


Run database migrations
~~~~~~~~~~~~~~~~~~~~~~~

The database will need to be migrated before you can start any application development work:

..  code-block:: bash

    docker-compose run web python manage.py migrate


Deployment and further development
-----------------------------------------

The project can be committed using Git, and deployed using the Divio CLI or the Control Panel in the usual way.

It would make sense to add an appropriate ``.gitignore`` file to keep things clean, such as:

..  code-block:: text

    # macOS
    .DS_Store
    .DS_Store?
    ._*
    .Spotlight-V100
    .Trashes

    # Python
    *.pyc
    *.pyo
    db.sqlite3

    # Django
    /staticfiles

    # Divio
    .divio
    /data.tar.gz
    /data


Notes on working with the project
---------------------------------

Using the Twelve-factor model places all configuration in environment variables, so that the project can readily be
moved to another host or platform, or set up locally for development. The configuration for:

* security
* database
* media
* static files

settings is handled by a few simple code snippets in ``settings.py``. In each case, the settings will fall back to
safe and secure defaults.


Application container
~~~~~~~~~~~~~~~~~~~~~

In both local and cloud environments, the application will run in a ``web`` container, using the same image and
exactly the same codebase.


.. _django-create-deploy-startup:

Django server
~~~~~~~~~~~~~

In cloud environments: the ``Dockerfile`` contains a ``CMD`` that starts up Django using the uWSGI/Gunicorn/Uvicorn
application gateway server.

In the local environment: the ``command`` line in ``docker-compose.yml`` starts up Django using the runserver,
overriding the ``CMD`` in the ``Dockerfile``. If the ``command`` line is commented out, ``docker-compose up`` will use
the application gateway server locally instead.


Database
~~~~~~~~

In cloud environments: the application will use one of our database clusters.

In the local environment: the application will use a container running the same database.

During the build phase: the database falls back to in-memory SQLite, as there is no database available to connect to,
and no configuration variables available from the environment in any case.


Security settings
~~~~~~~~~~~~~~~~~

Debug mode
^^^^^^^^^^

In cloud environments: the application will safely fall back to ``DEBUG = False``.

In the local environment: ``.env-local`` supplies a ``DJANGO_DEBUG`` variable to allow Django to run in debug mode.


Secret key
^^^^^^^^^^

In cloud environments: a random ``SECRET_KEY`` variable is always provided and will be used.

In the local environment: where no ``SECRET_KEY`` environment variable is provided, the application will fall back to a
hard-coded key in ``settings.py``.


Allowed hosts
^^^^^^^^^^^^^

In cloud environments: ``DOMAIN`` and ``DOMAIN_ALIASES`` variable are always provided and will be used.

In the local environment: default values are provided via the ``DOMAIN_ALIASES`` environment variable in ``.env-local``.


Static files
~~~~~~~~~~~~

In cloud environments: the application gateway server and WhiteNoise are used.

In the local environment: static files are served by the Django runserver. By :ref:`running the application gateway
server locally <django-create-deploy-startup>` and enforcing ``DEBUG = False``, it can be tested with WhiteNoise in the
local environment.


Media files
~~~~~~~~~~~

In cloud environments: file storage and serving is handled by the S3 instance.

In the local environment: the local filesystem is used for storage, and Django's runserver is used to serve media. If a
cloud environment's ``DEFAULT_STORAGE_DSN`` is applied in the ``.env-local`` file, the local server will use the S3
instance instead.


Database migrations
~~~~~~~~~~~~~~~~~~~

In its current state, database migrations are not executed automatically in cloud deployments. After deploying changes
that require a database migration, you will need to run them manually in the cloud environment using SSH.
