.. meta::
   :description:
       This guide explains step-by-step how to create and deploy a Twelve-factor Django project including Postgres or
       MySQL, and cloud media storage using S3, with Docker.
   :keywords: Docker, Django, Postgres, MySQL, S3

..  _django-create-deploy:

How to create (or migrate) and deploy a Django project
===========================================================================================

This guide will take you through the steps to create a portable, vendor-neutral `Twelve-factor
<https://www.12factor.net/config>`_ Django project, either by building it from scratch or migrating an existing application. It includes configuration for:

* Postgres or MySQL database
* cloud media storage using S3
* static file handling using `WhiteNoise <http://whitenoise.evans.io>`_
* `uWSGI <https://uwsgi-docs.readthedocs.io>`_, `Gunicorn <https://docs.gunicorn.org>`_ or `Uvicorn
  <https://www.uvicorn.org>`_

and deployment using Docker.

This guide assumes that you are familiar with the basics of the Divio platform and have Docker and the Divio CLI
installed. If not, please start with :ref:`our complete tutorial for Django <introduction>`, or at least :ref:`ensure
that you have the basic tools in place <local-cli>`.


Create or edit the project files
--------------------------------

Start in a new directory, or in an existing Django project of your own.


The ``Dockerfile``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a file named ``Dockerfile``, adding:

..  code-block:: Dockerfile

    FROM python:3.8
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt

(change the version of Python if required).


..  _django-create-deploy-requirements:

Python requirements in ``requirements.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Dockerfile`` expects to find a ``requirements.txt`` file, so add one. Where indicated below, choose the
appropriate options to install the components for Postgres/MySQL, and uWSGI/Uvicorn/Gunicorn, for example:

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

You may have Python components of your own that need to be added.


Local container orchestration with ``docker-compose.yml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``docker-compose.yml`` file, :ref:`for local development purposes <docker-compose-local>`. This will replicate
the ``web`` image used in cloud deployments, allowing you to run the application in an environment as close to that of
the cloud servers as possible. Amongst other things, it will allow the project to use a Postgres or MySQL database
(choose the appropriate lines below) running in a local container, and provides convenient access to files inside the
containerised application.

..  code-block:: yaml
    :emphasize-lines: 21-

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
          - "database_default"
        env_file: .env-local

      database_default:
        # Select one of the following db configurations for the database
        image: postgres:9.6-alpine
        environment:
          POSTGRES_DB: "db"
          POSTGRES_HOST_AUTH_METHOD: "trust"
          SERVICE_MANAGER: "fsm-postgres"
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

As you will see above, the ``web`` service refers to an ``env_file`` containing the environment variables that will be
used in the local development environment. Create a ``.env-local`` file, containing:

..  code-block:: text
    :emphasize-lines: 1-3

    # Select one of the following for the database
    DATABASE_URL=postgres://postgres@database_default:5432/db
    DATABASE_URL=mysql://root@database_default:3306/db

    DEFAULT_STORAGE_DSN=file:///data/media/?url=%2Fmedia%2F
    DJANGO_DEBUG=True
    DOMAIN_ALIASES=localhost, 127.0.0.1
    SECURE_SSL_REDIRECT=False


Build with Docker
~~~~~~~~~~~~~~~~~

Now you can build the application containers locally:

..  code-block:: bash

    docker-compose build


Create or edit the Django project module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application can be run inside its container now and commands can be executed in the Docker environment. If this is
a new project you will need to create a new Django project module:

..  code-block:: bash

    docker-compose run web django-admin startproject myapp .

If you use a different name, or you're working on an existing Django project, you will need to change the reference to
``myapp`` in the :ref:`static settings <django-create-deploy-static>` and the ``Dockerfile``'s ``CMD`` line,
:ref:`below <django-create-deploy-CMD>`.


Configure ``settings.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit your settings file (for example, ``myapp/settings.py``), to add some code that will read configuration from
environment variables, instead of hard-coding it. Add some imports:

..  code-block:: python

    import os
    import dj_database_url
    from django_storage_url import dsn_configured_storage_class


Some security-related settings. The cloud environments will provide some of these values as environment variables where
appropriate; in all cases they will fall back to safe values if an environment variable is not provided:

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

    # Redirect to HTTPS by default, unless explicitly disabled
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT') != "False"


Configure database settings:

..  code-block:: python

    # Configure database using DATABASE_URL; fall back to sqlite in memory when no
    # environment variable is available, e.g. during Docker build
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite://:memory:')

    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}


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


Add a URL pattern for serving media files in local development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need to edit the project's ``urls.py`` (e.g. ``myapp/urls.py``):

..  code-block:: python
    :emphasize-lines: 1-2, 8-

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]

    if settings.DEBUG:
        urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))


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
    CMD gunicorn --bind=0.0.0.0:80 --forwarded-allow-ips="*" myapp.wsgi
    CMD uvicorn --host=0.0.0.0 --port=80 myapp.asgi:application

(Note that this assumes your Django project was named ``myapp``.)


Run database migrations
~~~~~~~~~~~~~~~~~~~~~~~

The database will need to be migrated before you can start any application development work:

..  code-block:: bash

    docker-compose run web python manage.py migrate

And create a Django superuser:

..  code-block:: bash

    docker-compose run web python manage.py createsuperuser

**Or**, you can import the database content from an existing database.


Check the local site
~~~~~~~~~~~~~~~~~~~~

You can now start up the site locally to test it:

..  code-block:: bash

    docker-compose up

and log into the admin at http://127.0.0.1:8000/admin.

All the site's configuration (Debug mode, ``ALLOWED_HOSTS``, database settings, etc) is being provided by the
environment variables in the ``.env-local`` file. On the cloud, the environment variables will be provided
automatically by each environment.


Deployment and further development
-----------------------------------------

Create a new project on Divio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the `Divio Control Panel <https://control.divio.com>`_ add a new project, selecting the *Build your own* option.


Add database and media services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new project does not include any additional services; they must be added manually. Use the *Services* menu to add a
Postgres or MySQL database to match your choice earlier, and an S3 object storage instance for media.


Connect the local project to the cloud project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your Divio project has a *slug*, based on the name you gave it when you created it. Run ``divio project list -g`` to
get your project's slug; you can also read the slug from the Control Panel.

Run:

..  code-block:: bash

    divio project configure

and provide the slug. (This creates a new file in the project at ``.divio/config.json``.)

If you have done this correctly, ``divio project dashboard`` will open the project in the Control Panel.


Configure the Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialise the project as a Git repository if it's not Git-enabled already:

..  code-block:: bash

    git init .


A ``.gitignore`` file is needed to exclude unwanted files from the repository. Add:

..  code-block:: text

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


    # OS-specific patterns - add your own here
    .DS_Store
    .DS_Store?
    ._*
    .Spotlight-V100
    .Trashes

Add the project's Git repository as a remote, using the *slug* value in the remote address:

..  code-block:: bash

    git remote add origin git@git.divio.com:<slug>.git

(Use e.g. ``divio`` instead if you already have a remote named ``origin``.)


Commit your work
~~~~~~~~~~~~~~~~

..  code-block:: bash

    git add .                                                 # add all the newly-created files
    git commit -m "Created new project"                       # commit
    git push --set-upstream --force origin [or divio] master  # push, overwriting any unneeded commits made by the Control Panel at creation time

You'll now see "1 undeployed commit" listed for the project in the Control Panel.


Deploy the Test server
~~~~~~~~~~~~~~~~~~~~~~

Deploy with:

..  code-block:: bash

    divio project deploy

(or use the **Deploy** button in the Control Panel).

Once deployed, your project will be accessible via the Test server URL shown in the Control Panel (append ``/admin``).


Working with the database on the cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your cloud project does not yet have any content in the database, so you can't log in or do any other work there.
You can push the local database with the superuser you created to the Test environment:

..  code-block:: bash

    divio project push db

or, use the SSH URL available in the Test environment pane to open a session in a cloud container, and execute
Django migrations and create a superuser there in the usual way.

You can run migrations automatically on deployment by adding a :ref:`release command <release-commands>` in the Control
Panel.


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

In its current state, database migrations are not executed automatically in cloud deployments. To run migrations
automatically, add a :ref:`release command <release-commands>`: ``python manage.py migrate``. Alternatively you can run
the command manually in the cloud environment using SSH.
