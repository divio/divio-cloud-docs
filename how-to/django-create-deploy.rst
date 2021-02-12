.. meta::
   :description:
       This guide explains step-by-step how to deploy a Twelve-factor Django project including Postgres or
       MySQL, and cloud media storage using S3, with Docker.
   :keywords: Docker, Django, Postgres, MySQL, S3

..  _django-create-deploy:

How to migrate (or create) and deploy a Django project
===========================================================================================

This guide will take you through the steps to deploy a portable, vendor-neutral `Twelve-factor
<https://www.12factor.net/config>`_ Django project. It includes configuration for:

* Postgres or MySQL database
* cloud media storage using S3
* static file handling using `WhiteNoise <http://whitenoise.evans.io>`_
* `uWSGI <https://uwsgi-docs.readthedocs.io>`_, `Gunicorn <https://docs.gunicorn.org>`_ or `Uvicorn
  <https://www.uvicorn.org>`_

and deployment using Docker.

This guide assumes that you are familiar with the basics of the Divio platform and have Docker and the Divio CLI
installed. If not, please start with :ref:`our complete tutorial for Django <introduction>`, or at least :ref:`ensure
that you have the basic tools in place <local-cli>`.


Edit (or create) the project files
-----------------------------------

Start in an existing Django project, or if necessary, create a new directory.


The ``Dockerfile``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a file named ``Dockerfile``, adding:

..  code-block:: Dockerfile

    FROM python:3.8
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt

Change the version of Python if required; you can also specify the underlying operating system components according
to your requirements - see :ref:`manage-base-image-choosing`.


..  _django-create-deploy-requirements:

Python requirements in ``requirements.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Dockerfile`` expects to find a ``requirements.txt`` file, so add one if required. Where indicated below, choose
the appropriate options to install the components for Postgres/MySQL, and uWSGI/Uvicorn/Gunicorn, for example:

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

Check that the version of Django is correct, and include any other Python components required by your project.


..  _django-create-deploy-docker-compose:

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
        # the default command to run whenever the container is launched
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


..  _django-create-deploy-env-local:

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


Create a minimal Django project if required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to create a new Django project, you can run the ``startproject`` command inside the Docker application's
container:

..  code-block:: bash

    docker-compose run web django-admin startproject myapp .


Configure ``settings.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit your settings file (for example, ``myapp/settings.py``), to add some code that will read configuration from
environment variables, instead of hard-coding it. Add some imports:

..  code-block:: python

    import os
    import dj_database_url
    from django_storage_url import dsn_configured_storage_class


..  _django-create-deploy-security:

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


..  _django-create-deploy-database:

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

..  _django-create-deploy-media:

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

Append to a command to the ``Dockerfile`` that will collect static files. Finally, depending which application gateway
server :ref:`you installed above <django-create-deploy-requirements>`, include the appropriate command to launch the
application when a container starts:

..  code-block:: Dockerfile
    :emphasize-lines: 3-6

    RUN python manage.py collectstatic --noinput

    # Select one of the following application gateway server commands
    CMD uwsgi --http=0.0.0.0:80 --module=myapp.wsgi
    CMD gunicorn --bind=0.0.0.0:80 --forwarded-allow-ips="*" myapp.wsgi
    CMD uvicorn --host=0.0.0.0 --port=80 myapp.asgi:application

(Note that this assumes your Django project was named ``myapp``.)


Run database migrations if required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The database may need to be migrated before you can start any application development work:

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


..  include:: /how-to/includes/connect-local-to-cloud.rst


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

Add the project's Git repository as a remote, using the value obtained from the ``divio project configure`` command above, for example:

..  code-block:: bash

    git remote add origin git@git.divio.com:django-project.git

(Use e.g. ``divio`` as the remote name instead if you already have a remote named ``origin``.)


Commit your work
~~~~~~~~~~~~~~~~

..  code-block:: bash

    git add .                                                 # add all the newly-created files
    git commit -m "Created new project"                       # commit
    git push --set-upstream --force origin [or divio] master  # push, overwriting any unneeded commits made by the Control Panel at creation time

You'll now see "1 undeployed commit" listed for the project in the Control Panel.


..  include:: /how-to/includes/django-deploy-test-working-database.rst


Additional notes
-----------------

See :ref:`working-with-recommended-django-configuration` for further guidance.
