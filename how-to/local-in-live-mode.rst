.. _local-in-live-mode:

How to run a local project in live configuration
================================================

The Local, Test and Live server environments are as identical as possible, to help guarantee
that your applications will run in just the same way across all of them.

However, there are a few differences. See :ref:`default-project-conditions` for the default
configuration in each environment.

Occasionally, you may wish to run the local server in a configuration closer to the live set-up. A
few steps are needed to achieve this.


Build the project
-----------------

Build the project in the normal way (``docker-compose build web``) if there have been any changes to it.


..  _local-live-volumes:

Disable the ``volumes`` behaviour in ``docker-compose.yml`` (optional)
-----------------------------------------------------------------------

If your ``Dockerfile`` includes commands it means that files in the project are processed at build time (say,
processing of static files before collection), the :ref:`default volumes configuration in the docker-compose.yml file
<docker-compose-volumes>` will cause this to be overwritten at run-time.

In such a case, comment out the line::

    - ".:/app:rw"

in ``docker-compose.yml``. Note that this means that further
changes you make to the project files on your host system will not be reflected inside the container until the
line is restored and the project is restarted.


Turn off Django ``DEBUG`` mode
------------------------------

Set a couple of :ref:`environment variables <environment-variables>` in the file ``.env-local``::

    DEBUG=False
    STAGE=live


Collect static files
--------------------

Gather static files to be served, using ``collectstatic``. Run::

    docker-compose run --rm web python manage.py collectstatic


Run the ``migrate`` command
---------------------------

Run::

    docker-compose run --rm web start migrate

This runs the commands listed in the ``MIGRATION_COMMANDS`` setting, populated by applications using the addons
framework, that are executed in Cloud deployments.


Use the production web server
-----------------------------

Use the production web server (using uWSGI, and serving static files) rather than the Django
runserver. In the :ref:`docker-compose.yml file <docker-compose-yml-reference>`, change::

    command: python manage.py runserver 0.0.0.0:80

to::

    command: start web

Now when you start the local server, it will behave more like the live server.
