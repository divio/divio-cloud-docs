.. meta::
   :description:
       This guide explains step-by-step how to create and deploy a Flask project with Docker, in accordance with
       Twelve-factor principles.
   :keywords: Docker, Flask, Postgres, MySQL, S3

..  _flask-create-deploy:

How to create (or migrate) and deploy a Flask project
===========================================================================================

This guide will take you through the steps to create a portable, vendor-neutral Flask project, either by building it
from scratch or migrating an existing application, and deploying it using Docker. The project architecture is in line
with `Twelve-factor <https://www.12factor.net/config>`_ design principles.

This guide assumes that you are familiar with the basics of the Divio platform and have Docker and the :ref:`Divio CLI
<local-cli>` installed.


Create or edit the project files
--------------------------------

Start in a new directory, or in an existing Flask project of your own.


Create a minimal application if required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may already have a Flask application of your own to migrate, but if not, the example below provides a minimal one.
The example is taken from the :doc:`Flask tutorial's own flaskr example <tutorial/factory>`. Create a ``flaskr``
directory, containing an ``__init__.py`` file:

..  code-block:: python
    :emphasize-lines: 10-12

    import os

    from flask import Flask


    def create_app(test_config=None):
        # create and configure the app
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_mapping(
            SECRET_KEY = os.environ.get('SECRET_KEY', 'dev'),
            DATABASE = os.environ.get('DATABASE_URL', os.path.join(app.instance_path, 'flaskr.sqlite'),
            STORAGE = os.environ.get('DEFAULT_STORAGE_DSN')
        )

        if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            app.config.from_mapping(test_config)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        # a simple page that says hello
        @app.route('/hello')
        def hello():
            return 'Hello, World!'

        return app

Note the highlighted sections above, in which the application obtains configuration values from its environment. If you
are working on your own application that has database or other configuration of this kind, you should adapt it so that
it is similarly able to obtain these values.

The next step is to Dockerise the application.


The ``Dockerfile``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a file named ``Dockerfile``, adding:

..  code-block:: Dockerfile
    :emphasize-lines: 6-8

    FROM python:3.8
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt

    # Select one of the following application gateway server commands
    CMD uwsgi --http=0.0.0.0:80 --module="flaskr:create_app()"
    CMD gunicorn --bind=0.0.0.0:80 --forwarded-allow-ips="*" "flaskr:create_app()"

You may need to change the version of Python, and should also select the ``CMD`` that will start your preferred gateway
server for production - if you're not using the ``flaskr`` example, you'll need to amend the name in the command too.


..  _flask-create-deploy-requirements:

Python requirements in ``requirements.txt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Dockerfile`` expects to find a ``requirements.txt`` file, so add one. Where indicated below, choose the
appropriate options to install the components for Postgres/MySQL if you plan to use them, and uWSGI/Gunicorn, for example:

..  code-block:: Dockerfile
    :emphasize-lines: 3-5, 7-9

    flask==1.1.2

    # Select one of the following for the database as required
    psycopg2==2.8.5
    mysqlclient==2.0.1

    # Select one of the following for the gateway server
    uwsgi==2.0.19.1
    gunicorn==20.0.4

You may have Python components of your own that need to be added.


Local container orchestration with ``docker-compose.yml``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``docker-compose.yml`` file, :ref:`for local development purposes <docker-compose-local>`. This will replicate
the ``web`` image used in cloud deployments, allowing you to run the application in an environment as close to that of
the cloud servers as possible. Amongst other things, it will allow the project to use a Postgres or MySQL database
running in a local container, and provides convenient access to files inside the containerised application.

You will need to include/delete the highlighted sections below appropriately:

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
        # the default command to run wheneve the container is launched
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


Local configuration using ``.env-local``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you will see above, the ``web`` service refers to an ``env_file`` containing the environment variables that will be
used in the local development environment. Create a ``.env-local`` file. As with the ``docker-compose.yml``, select
the ``DATABASE_URL`` as required.

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

With this, you have the basics for a Dockerised application that can equally effectively be deployed in a production environment or run locally, using environment variables for configuration in ether case.


Build with Docker
~~~~~~~~~~~~~~~~~

Now you can build the application containers locally:

..  code-block:: bash

    docker-compose build


Application configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

It's beyond the scope of this guide to cover configuration in detail, as that will depend to a great extent on the
application you have or are planning to build. However the basic principle for all configuration is similar:
exactly the same application code should run without modification whether locally or in one of the multiple cloud
environments, and all configuration should be provided by environment variables.

For example:


Database
^^^^^^^^

In the ``flaskr`` example above, the database configuration is read from the ``DATABASE_URL`` environment variable, and
falls back to use SQLite if not provided.

Each Divio cloud environment with a database attached to it will be provided automatically with a
``DATABASE_URL`` environment variable. In the ``.env-local`` and ``docker-compose.yml`` files above, example
configuration is provided so that when running locally, the application can use the same database type as it does in
production. (This is a much more satisfactory approach than using say Postgres in production and SQLite for
development.)


Media storage
^^^^^^^^^^^^^

If your application needs to handle media, it should parse the ``DEFAULT_STORAGE_DSN`` to configure an appropriate
storage interface. Each Divio cloud environment with media object storage provisioned will be provided with a
``DEFAULT_STORAGE_DSN`` variable.

Use ``DEFAULT_STORAGE_DSN`` in ``.env-local`` to configure storage for local development. This can be one of the cloud
storage instances, but it's often convenient to use local file storage rather than a cloud media store (as in the
example given, ``file:///data/media/?url=%2Fmedia%2F``) if your Flask code can handle both kinds of storage backend.


Serving static files
^^^^^^^^^^^^^^^^^^^^

For handling static files, various suitable options are available, including :doc:`whitenoise:index` - see
:doc:`whitenoise:flask`.


Other configuration
^^^^^^^^^^^^^^^^^^^

Divio cloud projects include :ref:`a number of environment variables as standard <env-var-list>`. In addition,
:ref:`user-supplied variables <environment-variables>` may be applied per-environment.


Check the local site
~~~~~~~~~~~~~~~~~~~~

To start up the site locally to test it:

..  code-block:: bash

    docker-compose up

and access it at http://127.0.0.1:8000/hello (if using the ``flaskr`` example).


.. _flask-create-deploy-startup:

Test using the production gateway server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In cloud environments: the ``Dockerfile`` contains a ``CMD`` that starts up Flask using the uWSGI/Gunicorn or other
application gateway server.

In the local environment: the ``command`` line in ``docker-compose.yml`` starts up Flask using the ``flask run``
command, overriding the ``CMD`` in the ``Dockerfile``. If the ``command`` line is commented out, ``docker-compose up``
will use the application gateway server locally instead.


Deployment and further development
-----------------------------------------

Create a new project on Divio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the `Divio Control Panel <https://control.divio.com>`_ add a new project, selecting the *Build your own* option.


Add database and media services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new project does not include any :ref:`additional services <services>`; they must be added manually using the Divio
Control Panel if required. Use the *Services* menu to add a Postgres or MySQL database to match your choice earlier,
and an S3 object storage instance for media.


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

Once deployed, your project will be accessible via the Test server URL shown in the Control Panel.
