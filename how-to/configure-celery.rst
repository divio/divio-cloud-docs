.. _configure-celery:

How to configure Celery
=======================

..  note::

    This article assumes that you are already familiar with the basics of using
    Celery with Django. If not, please see `Celery's documentation
    <http://www.celeryproject.org/docs-and-support/>`_.


Add Celery to your project
-------------------------------

In your project's subscription, add the number of Celery workers you require. You can start with just one and add more
later if required.

..  important::

    If your Test and Live servers have not yet been deployed, please deploy each of them. This is required before
    Celery can be provisioned on the project.

Celery will then be provisioned on your project's Test and Live servers by our infrastructure team. This includes the
installation of our `Aldryn Celery <https://github.com/aldryn/aldryn-celery>`_ addon, and configuration of new
:ref:`environment variables <celery-environment-variables>` your project will need.


About Aldryn Celery
~~~~~~~~~~~~~~~~~~~

Aldryn Celery is a wrapper application that `installs
<https://github.com/divio/aldryn-celery/blob/master/requirements.txt>`_ and configures Celery in your project, exposing
multiple Celery settings as `environment variables
<https://github.com/divio/aldryn-celery/blob/master/aldryn_config.py>`_ for fine-tuning its configuration.

You don't *need* to use Aldryn Celery to use Celery and Django Celery on Divio Cloud - you can of course install and
configure Celery components manually if you prefer, perhaps if you wish to use a version that we haven't provided
support for in Aldryn Celery. You will in that case need to:

* install the Celery components you need in your project's requirements file
* apply the settings we provide as :ref:`environment variables <celery-environment-variables>`.


Configure Celery for the local server
-------------------------------------

For development purposes you will need to set up Celery in the local environment too, in such a way that it reflects
the provision made on our Cloud.

In the following steps you will set up a number of local services using the :ref:`docker-compose.yml
<docker-compose-yml-reference>` file:

* ``rabbitmq`` - `RabbitMQ <http://www.rabbitmq.com>`_, a *broker service* responsible for the creation of task queues,
  assignment of tasks to queues and delivering tasks to workers
* ``celeryworker``; the worker(s) will execute the assigned tasks
* ``celerybeat``, a scheduling service for periodic tasks
* ``celerycam``, a monitoring service

Your project will already have at least two services, ``web`` and ``db``, listed in ``docker-compose.yml``. Each of the
new services will be need to be added in a similar way, so that each runs in its own Docker container locally. (On our
Cloud, they will run on our dedicated clusters, and the :ref:`docker-compose file is not used <docker-compose-local>`.)


RabbitMQ
~~~~~~~~

Set up the RabbitMQ messaging service, by adding the following lines:

..  code-block:: yaml
    :emphasize-lines: 9-17

    services:

      web:
        [...]

      db:
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
        - "db:postgres"
        - "rabbitmq:rabbitmq"
      volumes:
        - ".:/app:rw"
        - "./data:/data:rw"
      command: aldryn-celery worker
      env_file: .env-local

Rather than copying the example above, use the actual ``web`` service in your ``docker-compose`` file as its basis, in
case it contains other values that need to be present. Note that the ``ports`` option is **not** used.

The ``command`` option starts the worker process, and ``links`` provides a reference to the ``rabbitmq`` service.


Celery beat
~~~~~~~~~~~~~~~~

Celery beat needs to be set up in much the same way:

..  code-block:: yaml
    :emphasize-lines: 1, 5, 9

    celerybeat:
      build: "."
      links:
        - "db:postgres"
        - "rabbitmq:rabbitmq"
      volumes:
        - ".:/app:rw"
        - "./data:/data:rw"
      command: aldryn-celery beat
      env_file: .env-local


Celery cam
~~~~~~~~~~~~~~~~

And Celery cam:

..  code-block:: yaml
    :emphasize-lines: 1, 5, 9

    celerycam:
      build: "."
      links:
        - "db:postgres"
        - "rabbitmq:rabbitmq"
      volumes:
        - ".:/app:rw"
        - "./data:/data:rw"
      command: aldryn-celery cam
      env_file: .env-local


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


Run the local project
-------------------------

Build the newly-configured project::

  docker-compose build

Now ``docker-compose up`` or ``divio project up`` will start the services that Celery requires.

Note that although the Django runserver in your ``web`` container will restart automatically to load new code whenever
you make changes, that will not apply to the other services.

These will need to be restarted manually, for example by stopping and restarting the local project or by running
``docker-compose restart``. (Usually, only the ``celeryworker`` container needs to be restarted, so you can do
``docker-compose restart celeryworker``.)


Testing
-------

It's not within the scope of this documentation to explain how to get started with or use Celery, but as a quick check
that you have configured your local environment correctly, you can create a small Celery task in your project, in a new
``tasks_app`` application.

In the root of your project, add the application::

    tasks_app/
        __init__.py
        tasks.py

And in the ``tasks.py`` file:

..  code-block:: Python

    from celery.task import task
    from aldryn_celery.celery import app

    @app.task()
    def add(x, y):
        return x + y


Note that we are using Aldryn Celery's ready configured code here for convenience - otherwise, you would follow the
steps as described in the `First steps with Django
<http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html>`_ from the Celery documentation.

And finally, add ``"tasks_app"`` to ``INSTALLED_APPS`` in ``settings.py``.

Restart the ``celeryworker`` container, and start a new Django shell with::

    docker-compose run --rm web python manage.py shell

Then in the shell::

    >>> from tasks_app.tasks import add
    >>> result = add.delay(2, 3)

``result`` is a Celery ``AsyncResult`` instance, so you can get the return value::

    >>> result.get(timeout=1)
    5

If that works successfully, you have created a task, and been able to use RabbitMQ to send it to a waiting Celery
worker.

See the `Celery documentation <http://www.celeryproject.org/docs-and-support/>`_ for more information.


.. _celery-environment-variables:

Environment variables
---------------------

When Celery is enabled for your project, two new environment variables will be configured:

* ``BROKER_URL``
* ``RABBITMQ_ERLANG_COOKIE``

The Test and Live servers will have different values for both.

Other environment variables used by Aldryn Celery can be found in its `aldryn_config.py
<https://github.com/aldryn/aldryn-celery/blob/master/aldryn_config.py>`_.

If you change environment variables locally, the containers will need to be stopped and restarted in order to pick up
the changes.
