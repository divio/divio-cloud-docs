.. raw:: html

    <style>
        table.docutils { width: 100%; table-layout: fixed;}
        table.docutils th, table.docutils td { white-space: normal }
    </style>

.. _celery:
.. _configure-celery:

How to configure Celery
=======================


This article assumes that you are already familiar with the basics of using Celery with Django and that you have Celery installed
in your application.

If not, please see :doc:`Celery's documentation <celery:index>`.


Add a Celery service to your application
----------------------------------------

In the application's subscription, add the number of Celery workers you require. You can start with just one and add
more later if required.

..  important::

    If your environments have not yet been deployed, please deploy each of them. This is required before
    Celery can be provisioned on the application.

Celery will then be provisioned for your application's environments by our infrastructure team. This includes
configuration of new :ref:`environment variables <celery-environment-variables>` it will need.

Once provisioned and deployed, your cloud application will run with new Docker instances for the Celery workers. The containers
running Celey components use the same image as the web container, but are started up with a different command.

We provide various cloud containers for Celery:

* Celery worker containers (multiple containers, according to the subscription)
* a :ref:`Celery beat <celery:guide-beat>` container, to handle scheduling
* a :ref:`Celery camera <celery:monitoring-snapshots>`, to provide snapshots for monitoring

Note that if your Divio application is on a plan that pauses due to inactivity, this will also pause the Celery containers.


Application configuration
--------------------------

Your application needs configuration to:

* read the environment variables we supply and use them as values for configuring Celery
* start up each Celery container correctly
* for local development, run Celery's workers in their own containers to replicate the cloud configuration

These tasks are covered in order below.


Using the broker environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For Celery, we provide a ``DEFAULT_AMQP_BROKER_URL`` (in some older applications, simply ``BROKER_URL``). This provides
configuration details for the AMQP message queue that handles Celery tasks. It's in the form:

..  code-block:: text

    transport://userid:password@hostname:port/virtual_host

This configuration will need to be passed to Celery for its :ref:`broker settings <celery:conf-broker-settings>` (``CELERY_BROKER_URL``,
for Django).

For applications using Aldryn Celery
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Aldryn Celery will take care of configuration. See :ref:`aldryn-celery` below.


.. _how-to-celery-startup:

Starting the cloud containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As noted above, these containers are all instances of the same application image, but are started up by different commands.

For the worker and scheduling containers, your application needs an executable at ``/usr/local/bin/aldryn-celery``, containing:

..  code-block:: bash

    #!/bin/shif

    [ $1 = "beat" ] ; then
        celery -A path.to.celery.app beat --loglevel=INFO
    else
        celery -A path.to.celery.app worker --concurrency=4 --loglevel=INFO --without-gossip --without-mingle --without-heartbeat -Ofair
    fi

Note the paths that you will need to specify yourself.

Similarly, on deployment the infrastructure invokes (by default) a Django management command ``python manage.py celerycam`` to
start up the monitoring container.

* If you don’t want to use a monitoring container, please inform us, so that we can configure your application to start up without
  issuing the command (deployments will fail if the command fails)
* If you do want to use a monitoring container, you will need to add a ``celerycam`` management command to your application. The
  command needs to respond to the invocation: ``python manage.py celerycam --frequency=10 --pidfile=``.

For an example of a ``celerycam`` management command implementation, see `how Aldryn Celery does this
<https://github.com/divio/aldryn-celery/blob/77886f934de9dd2d25b8279af8054b03c6677d03/aldryn_config.py#L57>`_ via the
``djcelery.snapshot.Camera`` class from the Django Celery library.

These entrypoints will be improved in future for developer convenience.


For applications using Aldryn Celery
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If using Aldryn Celery, an executable ``/usr/local/bin/aldryn-celery`` is provided.

Similarly, a  ``celerycam`` management command is implemented.

No further action is required on your part.

See :ref:`aldryn-celery` below.


Configure Celery for the local environment
-------------------------------------------

For development purposes you will need to set up Celery in your local environment too, in such a way that it reflects
the provision made on our cloud. A complete set-up would include:

.. list-table::
   :widths: 40 20 20 20
   :header-rows: 1

   * - function
     - handled by
     - on the cloud
     - local container name
   * - `AMPQ <http://www.amqp.org>`_ message broker service responsible for the creation of task queues
     - `RabbitMQ <http://www.rabbitmq.com>`_
     - `CloudAMPQ <https://www.cloudamqp.com>`_
     - ``rabbitmq``
   * - task execution
     - Celery workers
     - Celery containers
     - ``celeryworker``
   * - scheduling
     - :ref:`Celery beat <celery:guide-beat>`
     - Celery beat container
     - ``celerybeat``
   * - monitoring
     - :ref:`Celery snapshots <monitoring-snapshots>`
     - Celery camera container
     - ``celerycam``

Locally, the four new containers will be set up as new services using the :ref:`docker-compose.yml
<docker-compose-yml-reference>` file.

Note that in the cloud environment, the Celery-related containers are launched automatically. They, and the AMPQ message queue, are
not directly accessible. All monitoring and interaction must be handled via the main application running in the ``web``
container(s). The :ref:`docker-compose file is not used on the cloud <docker-compose-local>`.

Your application will already have other services listed in its ``docker-compose.yml``. Each of the new services will be need to be
added in a similar way.


RabbitMQ
~~~~~~~~

Set up the RabbitMQ messaging service, by adding the following lines:

..  code-block:: yaml
    :emphasize-lines: 9-17

    services:

      web:
        [...]

      database_default:
        [...]

      rabbitmq:
        image: rabbitmq:3.5-management
        hostname: rabbitmq
        ports:
          - "15672:15672"
        expose:
          - "15672"
        environment:
          RABBITMQ_ERLANG_COOKIE: secret_cookie_value

This uses the official `Docker RabbitMQ image <https://github.com/docker-library/rabbitmq>`_ (the
``rabbitmq:3.5-management`` image in turn installs ``rabbitmq:3.5``). It also gives the container a hostname
(``rabbitmq``), maps and exposes the management interface port (``15672``) and sets a ``RABBITMQ_ERLANG_COOKIE``
environment variable (the actual ``secret_cookie_value`` here doesn't matter too much - you're only using this locally).


Celery worker
~~~~~~~~~~~~~~~~

Next add a Celery worker service in the same way. This service needs to run a Django environment almost identical to
that used by the ``web`` service, as it will use the same codebase, need access to the same database and so on. Its
definition will therefore be very similar, with key changes noted here:

..  code-block:: yaml
    :emphasize-lines: 1, 5, 9

    celeryworker:
      build: "."
      links:
        - "database_default"
        - "rabbitmq:rabbitmq"
      volumes:
        - ".:/app:rw"
        - "./data:/data:rw"
      command: <startup command>
      env_file: .env-local

Rather than copying the example above, use the actual ``web`` service in your ``docker-compose`` file as its basis, in
case it contains other values that need to be present. There's no need for the ``ports`` option.

You will need to provide a ``<startup command>`` based on :ref:`the one used to start up the cloud workers <how-to-celery-startup>`.

For applications using Aldryn Celery, use ``command: aldryn-celery worker``.


Celery beat
~~~~~~~~~~~~~~~~

Celery beat needs to be set up in much the same way:

..  code-block:: yaml
    :emphasize-lines: 1, 5, 9

    celerybeat:
      build: "."
      links:
        - "database_default"
        - "rabbitmq:rabbitmq"
      volumes:
        - ".:/app:rw"
        - "./data:/data:rw"
      command: <startup command>
      env_file: .env-local

You will need to provide a ``<startup command>`` based on :ref:`the one used to start up the cloud scheduler
<how-to-celery-startup>`.

For applications using Aldryn Celery, use ``command: aldryn-celery beat``.


Celery cam
~~~~~~~~~~~~~~~~

And Celery cam:

..  code-block:: yaml
    :emphasize-lines: 1, 5, 9

    celerycam:
      build: "."
      links:
        - "database_default"
        - "rabbitmq:rabbitmq"
      volumes:
        - ".:/app:rw"
        - "./data:/data:rw"
      command: aldryn-celery cam
      env_file: .env-local

You will need to provide a ``<startup command>`` based on based on :ref:`the one used to start up the cloud monitoring container
<how-to-celery-startup>`., e.g. ``python manage.py celerycam --frequency=10 --pidfile=``.

For applications using Aldryn Celery, use ``command: aldryn-celery cam``.


The ``web`` service
~~~~~~~~~~~~~~~~~~~~~~~~

Finally, to the ``links`` option in ``web``, you also need to add the link to ``rabbitmq``:

..  code-block:: yaml
    :emphasize-lines: 5

    web:
      [...]
      links:
        [...]
        - "rabbitmq:rabbitmq"


Set up local environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``.env-local`` add::

    RABBITMQ_ERLANG_COOKIE=secret_cookie_value
    BROKER_URL="amqp://guest:guest@rabbitmq:5672/"

(Don't confuse the port ``5672`` of the RabbitMQ server with the port ``15672`` of its management interface.)


Run the local application
-------------------------

Build the newly-configured application::

    docker-compose build

Now ``docker-compose up`` will start the services that Celery requires.

Note that although the Django runserver in your ``web`` container will restart automatically to load new code whenever
you make changes, that will not apply to the other services.

These will need to be restarted manually, for example by stopping and restarting the local application or by running
``docker-compose restart``. (Usually, only the ``celeryworker`` container needs to be restarted, so you can do
``docker-compose restart celeryworker``.)

If you make any local changes to a application's configuration that need to be accessible to the Celery workers, run
``docker-compose build`` to rebuild them.


.. _celery-environment-variables:

Environment variables
---------------------

When Celery is enabled for your application, two new environment variables will be configured:

* ``BROKER_URL``
* ``RABBITMQ_ERLANG_COOKIE``

Different cloud environments will have different values for both.

The number of Celery workers per Docker instance can be configured with the
``CELERYD_CONCURRENCY`` environment variable. The default is 2. This can be
increased, but in that case, you will need to monitor your own RAM consumption
via the Control Panel.


For applications using Aldryn Celery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other environment variables used by Aldryn Celery can be found in its `aldryn_config.py
<https://github.com/aldryn/aldryn-celery/blob/master/aldryn_config.py>`_.


.. _aldryn-celery:

Aldryn Celery (legacy)
-------------------------

Aldryn Celery is an :ref:`Aldryn Addon <aldryn>` wrapper application that `installs
<https://github.com/divio/aldryn-celery/blob/master/requirements.txt>`_ and configures Celery in your application, exposing
multiple Celery settings as `environment variables <https://github.com/divio/aldryn-celery/blob/master/aldryn_config.py>`_ for
fine-tuning its configuration.

Aldryn Celery installs components including Celery itself and Django Celery. The addon is no longer updated, and installs an older
version of Celery. Applications currently using Aldryn Celery will eventually need to be updated to maintain compatibility with
other dependencies of the application.
