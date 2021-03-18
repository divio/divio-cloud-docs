.. meta::
   :description:
       This guide explains step-by-step how to deploy a application with Docker, in accordance with
       Twelve-factor principles.
   :keywords: Docker, Postgres, MySQL, S3

..  _deploy-generic:

How to deploy a web application on Divio: generic guide
===========================================================================================

..  include:: /how-to/includes/deploy-common-intro.rst

The steps outline here will work for an application based on any suitable framework and language. We also have more
detailed and specific guides that cover :ref:`Django <deploy-django>` and :ref:`Flask <deploy-flask>`.

..  include:: /how-to/includes/deploy-common-prerequisites.rst

..  include:: /how-to/includes/deploy-common-dockerfile.rst

..  include:: /how-to/includes/deploy-common-dockerfile-system-dependencies.rst

..  include:: /how-to/includes/deploy-common-dockerfile-application-dependencies.rst

As well as pinning known requirements, it's a good idea to pin all their secondary dependencies too. The
language environment you're using probably has a way to do this.

For example, in Python you can run ``pip freeze`` to get a definitive list of dependencies, or do something similar
in Node with ``npm shrinkwrap``.

..  include:: /how-to/includes/deploy-common-dockerfile-file-building.rst

..  _deploy-generic-cmd:

..  include:: /how-to/includes/deploy-common-dockerfile-cmd.rst

For example, for a Python Flask application you might use something like:

..  code-block:: Dockerfile

    CMD gunicorn --bind=0.0.0.0:80 --forwarded-allow-ips="*" "flaskr:create_app()"

..  include:: /how-to/includes/deploy-common-cmd-admonition.rst

..  include:: /how-to/includes/deploy-common-dockerfile-access-services.rst

..  include:: /how-to/includes/deploy-common-configuration-services.rst

..  include:: /how-to/includes/deploy-common-helper-modules.rst

Your chosen framework may already have helper module libraries available that can parse environment variables to extract the settings and apply them to the application (most mature and widely-used frameworks do). If not, you will need to parse the variables yourself.

..  include:: /how-to/includes/deploy-common-settings-security.rst

..  include:: /how-to/includes/deploy-common-settings-database.rst

Your own application should do something similar.

..  include:: /how-to/includes/deploy-common-settings-static.rst

If your application framework can handle file serving with a reasonable degree of efficiency, in most cases it is
perfectly adequate to serve them from the application, at least to begin with.

..  include:: /how-to/includes/deploy-common-settings-media.rst

For an example, see :ref:`how we recommend using the DEFAULT_STORAGE_DSN in a Django application
<deploy-django-media>`.

..  include:: /how-to/includes/deploy-common-settings-media-admonition.rst

..  include:: /how-to/includes/deploy-common-settings-other.rst

..  include:: /how-to/includes/deploy-common-compose.rst

..  code-block:: yaml
    :emphasize-lines: 13-14, 17, 24-

    version: "2.4"
    services:
      web:
        # the application's web service (container) will use an image based on our Dockerfile
        build: "."
        # map the internal port 80 to port 8000 on the host
        ports:
          - "8000:80"
        # map the host directory to app (which allows us to see and edit files inside the container)
        # /app assumes you're using that in the Dockerfile
        # /data is asuggestion for local media storage - see below
        volumes:
          - ".:/app:rw"
          - "./data:/data:rw"
        # an optional default command to run whenever the container is launched - this will override the Dockerfile's
        # CMD, allowing your application to run with a server suitable for development - this example is for Django
        command: python manage.py runserver 0.0.0.0:80
        # for the application's local db service
        links:
          - "database_default"
        env_file: .env-local

      database_default:
        # Select one of the following configurations for the database
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


..  include:: /how-to/includes/deploy-common-compose-env-local.rst

..  code-block:: text
    :emphasize-lines: 2-3

    # Select one of the following for the database
    DATABASE_URL=postgres://postgres@database_default:5432/db
    DATABASE_URL=mysql://root@database_default:3306/db

    # Storage will use local file storage in the data directory
    DEFAULT_STORAGE_DSN=file:///data/media/?url=%2Fmedia%2F

In cloud environments, we provide a number of useful variables. If your application needs to make use of them (see a
:ref:`Django example <deploy-django-security>`) you should provide them for local use too. For example:

..  code-block:: text

    DOMAIN_ALIASES=localhost, 127.0.0.1
    SECURE_SSL_REDIRECT=False

..  include:: /how-to/includes/deploy-compose-summary.rst

..  include:: /how-to/includes/deploy-common-buildrun-build.rst

..  include:: /how-to/includes/deploy-common-buildrun-run.rst

..  include:: /how-to/includes/deploy-common-git.rst

..  code-block:: text

    # used by the Divio CLI
    .divio
    /data.tar.gz

    # for local file storage
    /data

..  include:: /how-to/includes/deploy-common-deploy.rst
