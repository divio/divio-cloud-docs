.. _backend-services:

Backend services
==================

.. _celery:

Celery
------

..  admonition:: See also

    * :ref:`General information about Celery on Divio Cloud <configure-celery>`

Celery asynchronous task queue handling is available as a service, depending on
enabled project features.

Once enabled, your project will include four new Docker instances (two on the
Test and two on the Live server, unless otherwise arranged with Divio Cloud
support) each running the Celery workers.

The number of Celery workers per Docker instance can be configured with the
``CELERYD_CONCURRENCY`` environment variable. The default is 2. This can be
increased, but in that case, you will need to monitor your own RAM consumption
via the Control Panel.

Celery on Divio Cloud is handled by the `Aldryn Celery
<https://github.com/aldryn/aldryn-celery/blob/master/aldryn_config.py>`_ addon.
Please contact Divio Cloud support for custom queues, more instances or custom
queues.


Celery containers
~~~~~~~~~~~~~~~~~

The containers running the Celery workers are built using the same image as the
web container.


Celery on the Test server
~~~~~~~~~~~~~~~~~~~~~~~~~

Your project's Test server will pause after 15 minutes' inactivity in order to
save resources. This will also pause the Celery workers on the Test site.


Celery on the Local server
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you make any local changes to a project's configuration that need to be
accessible to the Celery workers, you should run ``docker-compose build`` to
rebuild them.

The Celery workers will need to be restarted after code changes, with::

    docker-compose restart celeryworker

If ``celeryworker`` seems to be taking too long to stop, run::

    docker-compose kill celeryworker
