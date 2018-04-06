.. _backend-services:

Backend services
==================

..  _media-storage:

Media storage and delivery
--------------------------

..  seealso::

    * :ref:`work-media-storage`
    * :ref:`interact-storage`

Default file storage on Divio Cloud projects is handled by dedicated storage and hosting providers.
These are `Amazon Web Services's S3 service <https://aws.amazon.com/s3/>`_, or a generic S3 hosting
service via another provider. Currently, most projects use Amazon's own S3 service, with the
exception of projects in our Swiss region.


.. _celery:

Celery
------

..  seealso::

    * :ref:`How to configure Celery on Divio Cloud <configure-celery>`

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
