.. meta::
   :description:
       This guide explains step-by-step how to set up a Twelve-factor Django application including Postgres or
       MySQL, and cloud media storage using S3, with Docker, for deployment on Divio.
   :keywords: Docker, Django, Postgres, MySQL, S3


.. _deploy-django:

How to configure an existing Django application for deployment on Divio
===========================================================================================

..  include:: /how-to/includes/deploy-common-intro.rst

The steps here should work with any Django project, and include configuration for:

* Postgres or MySQL database
* cloud media storage using S3
* static file handling using `WhiteNoise <http://whitenoise.evans.io>`_
* `uWSGI <https://uwsgi-docs.readthedocs.io>`_, `Gunicorn <https://docs.gunicorn.org>`_ or `Uvicorn
  <https://www.uvicorn.org>`_

..  include:: /how-to/includes/deploy-common-prerequisites.rst

If you don't already have a working Django project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`quickstart-django`.

..  include:: /how-to/includes/deploy-common-dockerfile.rst

For a Django application, you can use:

..  code-block:: Dockerfile

    FROM python:3.8

Here, ``python:3.8`` is the name of the Docker *base image*. We cannot advise on what base image you should use;
you'll need to use one that is in-line with your application's needs. However, once you have a working set-up, it's
good practice to move to a more specific base image - for example ``python:3.8.1-slim-buster``.

..  include:: /how-to/includes/deploy-common-dockerfile-base-images.rst

..  include:: /how-to/includes/deploy-common-dockerfile-system-dependencies.rst

..  include:: /how-to/includes/deploy-common-dockerfile-working-directory.rst

..  _deploy-django-requirements:

..  include:: /how-to/includes/deploy-common-dockerfile-application-dependencies.rst

..  code-block:: Dockerfile

    # install dependencies listed in the repository's requirements file
    RUN pip install -r requirements.txt

Any requirements should be pinned as firmly as possible.

Use the output from ``pip freeze`` to get a full list of dependencies. Assuming you use :ref:`the methods we recommend
below for configuring settings and handling storage <deploy-django-settings>`, you will need to include some of the
following (it's up to you to choose the right versions of course):

..  code-block:: text
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


..  include:: /how-to/includes/deploy-common-dockerfile-file-building.rst

A minimal Django application needs to have its static files collected:

..  code-block:: Dockerfile

    RUN python manage.py collectstatic --noinput


..  _deploy-django-cmd:

..  include:: /how-to/includes/deploy-common-dockerfile-cmd.rst

..  code-block:: Dockerfile

    # Select one of the following application gateway server commands
    CMD uwsgi --http=0.0.0.0:80 --module=myapp.wsgi
    CMD gunicorn --bind=0.0.0.0:80 --forwarded-allow-ips="*" myapp.wsgi
    CMD uvicorn --host=0.0.0.0 --port=80 myapp.asgi:application

You'll need to change ``myapp`` appropriately.


..  include:: /how-to/includes/deploy-common-cmd-admonition.rst

..  include:: /how-to/includes/deploy-common-dockerfile-access-services.rst

.. _deploy-django-settings:

..  include:: /how-to/includes/deploy-common-configuration-services.rst

..  include:: /how-to/includes/deploy-common-helper-modules.rst

In your Django settings file, import some helper modules to handle the environment variables:

..  code-block:: python

    import os
    import dj_database_url
    from django_storage_url import dsn_configured_storage_class


..  _deploy-django-security:

Security settings
~~~~~~~~~~~~~~~~~~~~~~~~~

Some security-related settings such as ``ALLOWED_HOSTS`` are required in Django. The cloud environments will provide
some of these values as environment variables where appropriate; in all cases the configuration we provide in this
example will fall back to safe values if an environment variable is not provided:

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
    DIVIO_DOMAIN_REDIRECTS = [
        d.strip()
        for d in os.environ.get('DOMAIN_REDIRECTS', '').split(',')
        if d.strip()
    ]

    ALLOWED_HOSTS = [DIVIO_DOMAIN] + DIVIO_DOMAIN_ALIASES + DIVIO_DOMAIN_REDIRECTS

    # Redirect to HTTPS by default, unless explicitly disabled
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT') != "False"


..  _deploy-django-database:

..  include:: /how-to/includes/deploy-common-settings-database.rst

For Django, we recommend:

..  code-block:: python

    # Configure database using DATABASE_URL; fall back to sqlite in memory when no
    # environment variable is available, e.g. during Docker build
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite://:memory:')

    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}

..  _deploy-django-static:

..  include:: /how-to/includes/deploy-common-settings-static.rst

For our recommended general-purpose static file serving configuration, first, add the ``WhiteNoiseMiddleware`` to the
list of ``MIDDLEWARE``, after the ``SecurityMiddleware``:

..  code-block:: python
    :emphasize-lines: 3

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        [...]
    ]

and then apply:

..  code-block:: python

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

..  _deploy-django-media:

..  include:: /how-to/includes/deploy-common-settings-media.rst

For Django, we suggest using:

..  code-block:: python

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

..  include:: /how-to/includes/deploy-common-settings-media-admonition.rst

..  include:: /how-to/includes/deploy-common-settings-other.rst

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


..  _deploy-django-docker-compose:

..  include:: /how-to/includes/deploy-common-compose.rst

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
        # a link to database_default, the application's local database service
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


..  _deploy-django-env-local:

..  include:: /how-to/includes/deploy-common-compose-env-local.rst

..  code-block:: text
    :emphasize-lines: 1-3

    # Select one of the following for the database
    DATABASE_URL=postgres://postgres@database_default:5432/db
    DATABASE_URL=mysql://root@database_default:3306/db

    DEFAULT_STORAGE_DSN=file:///data/media/?url=%2Fmedia%2F
    DJANGO_DEBUG=True
    DOMAIN_ALIASES=localhost, 127.0.0.1
    SECURE_SSL_REDIRECT=False

..  include:: /how-to/includes/deploy-common-compose-summary.rst

..  include:: /how-to/includes/deploy-common-buildrun-build.rst

Run database migrations if required
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new database will need to be migrated before you can start any application development work:

..  code-block:: bash

    docker-compose run web python manage.py migrate

And create a Django superuser:

..  code-block:: bash

    docker-compose run web python manage.py createsuperuser

**Or**, you can import the database content from an existing database - see :ref:`interact-database`.


..  include:: /how-to/includes/deploy-common-buildrun-run.rst

..  include:: /how-to/includes/deploy-common-git.rst

If using the suggestions above, you'll probably want:

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


Additional notes
-----------------

See :ref:`working-with-recommended-django-configuration` for further guidance.


..  include:: /how-to/includes/deploy-common-deploy.rst
