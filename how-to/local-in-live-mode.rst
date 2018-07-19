.. _local-in-live-mode:

How to run a local project in live configuration
================================================

The Local, Test and Live server environments are as identical as possible, to help guarantee
that your applications will run in just the same way across all of them.

However, there are a few differences. The default conditions are:

+--------------------------------+------------------+----------+------------------+
|                                |Local             | Test     | Live             |
+================================+==================+==========+==================+
| ``DEBUG`` environment variable | ``True``         |``True``  | ``False``        |
+--------------------------------+------------------+----------+------------------+
| ``STAGE`` environment variable | ``local``        | ``test`` | ``live``         |
+--------------------------------+------------------+----------+------------------+
| static files served by...      | Python runserver |  uWSGI                      |
+--------------------------------+                  +----------+------------------+
| media files served by...       |                  | our Cloud S3 service        |
+--------------------------------+------------------+----------+------------------+
| database runs in...            | a local container| our Cloud database cluster  |
+--------------------------------+------------------+----------+------------------+

Occasionally, you may wish to run the local server in a configuration closer to the live set-up.

A few steps are needed to achieve this.

Set some :ref:`environment variables <environment-variables>` in the file ``.env-local``::

    DEBUG=False
    STAGE=live

Gather static files to be served, using ``collectstatic``. Run::

    docker-compose run --rm web python manage.py collectstatic

Use the production web server (using uWSGI, and serving static files) rather than the Django
runserver. In the :ref:`docker-compose.yml file <docker-compose-yml-reference>`, change::

    command: python manage.py runserver 0.0.0.0:80

to::

    command: start web

Now when you start the local server, it will behave more like the live server.
