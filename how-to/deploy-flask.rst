.. meta::
   :description:
       This guide explains step-by-step how to deploy a Flask project with Docker, in accordance with
       Twelve-factor principles.
   :keywords: Docker, Flask, Postgres, MySQL, S3

..  _deploy-flask:

How to deploy a Flask application on Divio
===========================================================================================

..  include:: /how-to/includes/deploy-common-intro.rst

The steps here should work with any Flask project, and include configuration for:

* Postgres or MySQL database
* cloud media storage using S3
* static file handling using `WhiteNoise <http://whitenoise.evans.io>`_
* configuring a gateway server.


..  include:: /how-to/includes/deploy-common-prerequisites.rst

..  include:: /how-to/includes/deploy-common-dockerfile.rst

..  include:: /how-to/includes/deploy-common-dockerfile-system-dependencies.rst

..  include:: /how-to/includes/deploy-common-dockerfile-application-dependencies.rst

The ``requirements.txt`` file should pin Python dependencies as firmly possible (use the output from ``pip
freeze`` to get a full list). You will probably need to include some of the following:

..  code-block:: Dockerfile
    :emphasize-lines: 1-3, 5-7

    # Select one of the following for the database as required
    psycopg2==2.8.5
    mysqlclient==2.0.1

    # Select one of the following for the gateway server
    uwsgi==2.0.19.1
    gunicorn==20.0.4

Check that the version of Flask is correct, and include any other Python components required by your project.


..  include:: /how-to/includes/deploy-common-dockerfile-file-building.rst

..  include:: /how-to/includes/deploy-common-dockerfile-cmd.rst

..  code-block:: Dockerfile

    # Select one of the following application gateway server commands
    CMD uwsgi --http=0.0.0.0:80 --module="flaskr:create_app()"
    CMD gunicorn --bind=0.0.0.0:80 --forwarded-allow-ips="*" "flaskr:create_app()"


..  include:: /how-to/includes/deploy-common-cmd-admonition.rst

..  include:: /how-to/includes/deploy-common-dockerfile-access-services.rst

..  include:: /how-to/includes/deploy-common-configuration-services.rst

Helper modules
~~~~~~~~~~~~~~~~~~~~~~~~~

There are various Python helper module libraries available that can parse environment variables to
extract the settings so that you can apply them to the application.

..  include:: /how-to/includes/deploy-common-settings-security.rst

..  include:: /how-to/includes/deploy-common-settings-database.rst

..  include:: /how-to/includes/deploy-common-settings-static.rst

One option for Flask is to configure the webserver/gateway server to handle them; using Flask's own
``send_from_directory()`` can also be used, or :doc:`whitenoise:index` - see :doc:`whitenoise:flask`.

..  include:: /how-to/includes/deploy-common-settings-media.rst

..  include:: /how-to/includes/deploy-common-settings-media-admonition.rst

..  include:: /how-to/includes/deploy-common-settings-other.rst

..  include:: /how-to/includes/deploy-common-compose.rst

..  code-block:: yaml
    :emphasize-lines: 15-17, 20-

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
        command: flask run --host=0.0.0.0 --port=80
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


..  include:: /how-to/includes/deploy-common-env-local.rst

The ``FLASK_APP`` variable is used by the ``flask run`` command. It assumes that your application can be found at ``flaskr``; amend this appropriately if required.

..  code-block:: text
    :emphasize-lines: 1-3, 9

    # Select one of the following for the database
    DATABASE_URL=postgres://postgres@database_default:5432/db
    DATABASE_URL=mysql://root@database_default:3306/db

    DEFAULT_STORAGE_DSN=file:///data/media/?url=%2Fmedia%2F
    DOMAIN_ALIASES=localhost, 127.0.0.1
    SECURE_SSL_REDIRECT=False

    FLASK_APP=flaskr
    FLASK_ENV=development

With this, you have the basics for a Dockerised application that can equally effectively be deployed in a production
environment or run locally, using environment variables for configuration in ether case.


..  include:: /how-to/includes/deploy-common-buildrun-build.rst

..  include:: /how-to/includes/deploy-common-buildrun-run.rst

..  include:: /how-to/includes/deploy-common-git.rst

..  code-block:: text

    # Python
    *.pyc
    *.pyo
    db.sqlite3

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

..  include:: /how-to/includes/deploy-common-deploy.rst