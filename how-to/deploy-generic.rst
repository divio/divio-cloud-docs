.. meta::
   :description:
       This guide explains step-by-step how to deploy a project with Docker, in accordance with
       Twelve-factor principles.
   :keywords: Docker, Postgres, MySQL, S3

..  _deploy-generic:

How to migrate a generic web application to Divio
===========================================================================================

This guide will take you through the steps to deploy a portable, vendor-neutral project, based on any suitable
application stack, to Divio. The project architecture is in line with `Twelve-factor <https://www.12factor.net/config>`_
design principles.

This guide assumes that you are familiar with the basics of the Divio platform and Docker, and have Docker and the
:ref:`Divio CLI <local-cli>` installed.

It also assumes that you have a working project, containing at least a minimal web application, ready to be migrated.

We have more detailed and specific guides that cover :ref:`Django <deploy-django>` and :ref:`Flask
<deploy-flask>`.


Create a ``Dockerfile``
-----------------------

Your project may already include a ``Dockerfile``, in which case you are already some way along the road. Your
``Dockerfile`` needs to define an image in the usual way.

It's completely beyond the scope of this documentation to advise on what base image to use. However, `we provide a
number of images on Docker Hub <https://hub.docker.com/r/divio/base/tags?page=1&ordering=last_updated>`_, and you can
use many others.

We recommend setting up a working directory early on in the ``Dockerfile`` before you need to write any files, for
example:

..  code-block:: Dockerfile

    WORKDIR /app
    COPY . /app


Your ``Dockerfile`` should also include an entrypoint that launches a server running on port 80.
Usually, this will be a ``CMD`` at the end of the ``Dockerfile``.

For example, for a Python Flask project you might use something like:

..  code-block:: Dockerfile

    CMD gunicorn --bind=0.0.0.0:80 --forwarded-allow-ips="*" "flaskr:create_app()"

The ``Dockerfile`` will build the image that is used for all of the application's containers. It should for example
contain commands to install all the components required in the application.

During the build process, Docker has no access to to the application's environment or services. This means you cannot
run database operations such as migrations during the build process (these should be handled later as :ref:`release
commands <release-commands>`).

If the application needs to do things like generate static files, the best time to do that is during the build process.
This way they can be built into the image, so that all containers will have access to them.


Configuring your application to use services
----------------------------------------------

The application that is launched needs to be able to use any services such as database, media storage and so on. Divio
provides them, but your application needs the credentials to access them. For each service in each environment, we
provide an :ref:`environment variable <environment-variables>` containing the values. These can be found in the Env
variables view of the project.

Your application should:

* read the variables
* parse them to obtain the various credentials they contain
* configure its access to services using those credentials

You may be used to hard-coding such values in the application, for example in a settings or configuration file. Though
you can do this on Divio, we recommend not doing it.


Examples
~~~~~~~~~~~

The database credentials are provided in a ``DATABASE_URL`` environment variable  , in the form::

    schema://<user name>:<password>@<address>:<port>/<name>

An example of how we recommend making use of them in Django applications:

..  code-block:: python

    # Configure database using DATABASE_URL; fall back to sqlite in memory when no
    # environment variable is available, e.g. during Docker build

    import dj_database_url
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite://:memory:')
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}

Media credentials are similarly provided in ``DEFAULT_STORAGE_DSN``; see :ref:`how we recommend using them in a Django
application <deploy-django-media>`, and :ref:`more details of the storage DSN variable itself
<storage_access_details>`.


Media storage
~~~~~~~~~~~~~

Frameworks such as Django make it very straightforward to use multiple file storage backends; there are mature and
well-supported libraries that will let you use a Divio-provided S3 or MS Azure storage service. Whatever language or
software you're using, you will need ensure that your application is able to use the appropriate storage.

..  admonition:: Local file storage is not a suitable option

    Your code may expect, by default, to be able to write and read files from local file storage (i.e. files in the
    same file-space as belonging to the application).

    **This will not work well on Divio** or any similar platform. Our stateless containerised application model does
    not provide persistent file storage.

    Instead, your code should use a dedicated file storage; we provide AWS S3 and MS Azure blob storage options.


Local container orchestration with ``docker-compose.yml``
---------------------------------------------------------------------

What's described above is fundamentally all you need in order to deploy your application to Divio. However, a large
part of the value of Divio is the way it allows you to run the same application, in a very similar environment, locally
on your own computer, and the helper tools we provide. This makes development and testing much more productive. This is
what we'll consider here.

..  admonition:: ``docker-compose.yml`` is **only** used locally

    Cloud deployments do not use Docker Compose. Nothing that you do here will affect the way your application runs
    in a cloud environment. See :ref:`docker-compose-yml-reference`.

You will need a ``docker-compose.yml`` file that looks something like the one below. This one replicates the ``web``
image used in cloud deployments, allowing you to run the application in an environment as close to that of the cloud
servers as possible. It also allows the project to use a Postgres or MySQL database running in a local container, and
provides convenient access to files inside the containerised application. You will need to make some changes; pay attention to the highlighted sections:

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


Local configuration using ``.env-local``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you will see above, the ``web`` service refers to an ``env_file`` containing the environment variables that will be
used in the local development environment.

Divio cloud projects include :ref:`a number of environment variables as standard <env-var-list>`. In addition,
:ref:`user-supplied variables <environment-variables>` may be applied per-environment.

If the application refers to its environment for variables to configure database, storage or other services, it will
need to find those variables even when running locally. On the cloud, the variables will provide configuration details
for our database clusters, or media storage services. Clearly, you don't have a database cluster or S3 instance running
on your own computer, but Docker Compose can provide a suitable database running locally, and you can use local file
storage while developing.

Create a ``.env-local`` file. In this you need to provide some environment variables that are suitable for the
local environment:

..  code-block:: text

    # Select one of the following for the database
    DATABASE_URL=postgres://postgres@database_default:5432/db
    DATABASE_URL=mysql://root@database_default:3306/db

    # Storage will use local file storage in the data directory
    DEFAULT_STORAGE_DSN=file:///data/media/?url=%2Fmedia%2F

In cloud environments, we provide a number of useful variables. If your application makes use of them (see a
:ref:`Django example <deploy-django-security>`) you should provide them for local use too.
For example:

..  code-block:: text

    DOMAIN_ALIASES=localhost, 127.0.0.1
    SECURE_SSL_REDIRECT=False

With this, you have the basics for a Dockerised application that can equally effectively be deployed in a production environment or run locally, using environment variables for configuration in either case.


Building and running
--------------------

Build with Docker
~~~~~~~~~~~~~~~~~

Now you can build the application containers locally:

..  code-block:: bash

    docker-compose build

You may need to do additional steps such as migrating a database. To run a command inside the Dockerised environment,
precede it with ``docker-compose run web``. For example, to run Django migrations: ``docker-compose run web python
manage.py migrate``.


Check the local site
~~~~~~~~~~~~~~~~~~~~

To start up the site locally to test it:

..  code-block:: bash

    docker-compose up

and access it at http://127.0.0.1:8000/.


Git
--------------------

Your code needs to be in a Git repository so it can be pushed to Divio.

You will probably want to exclude some files from the Git repository, so check your ``.gitignore`` - if
using the suggestions above, you'll probably want to add some entries:

..  code-block:: text

    # used by the Divio CLI
    .divio
    /data.tar.gz

    # for local file storage
    /data


Deployment and further development
-----------------------------------------

Create a new project on Divio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the `Divio Control Panel <https://control.divio.com>`_ add a new project, selecting the *Build your own* option.


Add database and media services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new project does not include any :ref:`additional services <services>`; they must be added manually using the Divio
Control Panel if required. Use the *Services* menu to add a Postgres or MySQL database as required,
and an S3 or MS Azure object storage instance for media.


..  include:: /how-to/includes/connect-local-to-cloud.rst



Configure the Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the project's Git repository as a remote, using the value obtained from the ``divio project configure`` command above. For example:

..  code-block:: bash

    git remote add divio git@git.divio.com:my-divio-project.git


Commit and push
~~~~~~~~~~~~~~~~

Commit and push your work. You will need to force push to overwrite the initial commits in a Divio project if you're
using the ``master`` branch.


Deploy the Test server
~~~~~~~~~~~~~~~~~~~~~~

Deploy with:

..  code-block:: bash

    divio project deploy

(or use the **Deploy** button in the Control Panel).

Once deployed, your project will be accessible via the Test server URL shown in the Control Panel.
