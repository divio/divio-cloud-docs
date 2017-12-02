.. _configure-celery:

How to configure Celery
=======================

..  admonition:: See also

    * :ref:`celery`


..  note::

    This article assumes that you are already familiar with the basics of using
    Celery with Django. If not, please see `Celery's documentation
    <http://www.celeryproject.org/docs-and-support/>`_.


Request Celery for your project
-------------------------------

Celery needs to be set up by our infrastructure team. See :ref:`Celery on Divio
Cloud <celery>` for more information.

Your project will be set up with two new environment variables:

* ``BROKER_URL``
* ``RABBITMQ_ERLANG_COOKIE``

Test and Live servers will have different values for both.


Configure Celery in Cloud projects
----------------------------------

`Aldryn Celery's aldryn_config.py
<https://github.com/aldryn/aldryn-celery/blob/master/aldryn_config.py>`_ file
contains a number of settings that can be configured as environment variables.


Configure Celery for the local server
-------------------------------------

Set up Docker services
~~~~~~~~~~~~~~~~~~~~~~

You will need to add some new services to your :ref:`docker-compose.yml
<docker-compose-yml-reference>` file.


RabbitMB
^^^^^^^^

Set up the `RabbitMQ messaging service <http://www.rabbitmq.com>`_:

..  code-block:: yaml

    rabbitmq:
      image: rabbitmq:3.5-management
      hostname: rabbitmq
      ports:
        - "15672:15672"
      expose:
        - "15672"
      environment:
        RABBITMQ_ERLANG_COOKIE: <secret cookie value>


Celery worker
^^^^^^^^^^^^^

Set up the Celery worker service, with a ``command`` option to start the
worker process:

..  code-block:: yaml

    celeryworker:
      command: aldryn-celery worker

You will also need to add all of the other options already applied to the
``web`` service in the same file, except the ``ports`` option.

To the ``links`` option, add::

    - "rabbitmq:rabbitmq"

In other words, the ``celery`` service should now include something like:

..  code-block:: yaml
    :emphasize-lines: 3-

    celeryworker:
      command: aldryn-celery worker
      build: .
      links:
       - "db:postgres"
       - "rabbitmq:rabbitmq"
      volumes:
       - ".:/app:rw"
       - "./  data:/data:rw"
      env_file: .env-local

These are required because the ``celeryworker`` needs access to the same Python
components and environment as the web applications.


Celery beat
^^^^^^^^^^^

The `Celery beat scheduling service
<http://divio-cloud-developer-handbook.readthedocs.io/en/latest/reference/addons
-aldryn-sso.html>`_ needs to be set up in much the same way.

..  code-block:: yaml

    celerybeat:
      command: aldryn-celery beat

Copy over the other options from ``celeryworker``.


Celery cam
^^^^^^^^^^

The ``cam`` service captures events for monitoring purposes.

Add:

..  code-block:: yaml

    celerycam:
      command: aldryn-celery cam

followed once again by the other options from ``celeryworker``.


The ``web`` service
^^^^^^^^^^^^^^^^^^^

Finally, to the ``links`` option in ``web``, add::

    - "rabbitmq:rabbitmq"


Set up local environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``.env-local`` add::

    RABBITMQ_ERLANG_COOKIE=<secret cookie value>
    BROKER_URL="amqp://guest:guest@rabbitmq:5672/"


Running the local project
~~~~~~~~~~~~~~~~~~~~~~~~~

``docker-compose up`` or ``divio project up`` will now also start Celery.


Environment variable changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you change environment variables locally, the containers will need to be
stopped and restarted in order to pick up the changes.


Configuration changes
^^^^^^^^^^^^^^^^^^^^^

When making project configuration changes, you will need to rebuild all
the containers::

    docker-compose build


Code changes
^^^^^^^^^^^^

Unlike the ``web`` container, Celery's containers will not be reloaded on
Python code changes, so you will need to run ``docker-compose restart
celeryworker`` manually when required (the other containers shouldn't generally
need to be restarted).
