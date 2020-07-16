..  This include is used by:

    * django-03-setup-project-locally.rst
    * wagtail-03-setup-project-locally.rst
    * laravel-03-setup-project-locally.rst


If you open a new terminal window and run:

..  code-block:: bash

    docker ps

it will show you the Docker processes that are running - you will see something like (note that the details will
differ):

..  code-block:: text

    ➜ docker ps
    CONTAINER ID  IMAGE                COMMAND                 CREATED         STATUS        PORTS                 NAME
    d6007edbaf32  tutorialproject_web  "/tini -g -- pytho..."  17 minutes ago  Up 8 seconds  0.0.0.0:8000->80/tcp  tutorialproject_web_
    27ff3e661027  postgres:9.6         "docker-entrypoint..."  17 minutes ago  Up 8 seconds  5432/tcp              tutorialproject_db_

The first container is an instance of the image that you built, just like the one in the cloud deployment. The second
is the database, running in its own Docker container.

Once you have successfully logged into the local site, stop the project, using ``CONTROL-C``.


Useful commands
----------------------------------------

So far, we have used the ``divio``, ``docker-compose`` and ``docker`` commands. It's good to have a basic familiarity
with them and what they do. As you proceed through this tutorial, you may encounter the occasional issue. These
commands will help you when this happens.

..  note::

    See `our local commands cheat sheet <https://docs.divio.com/en/latest/reference/local-commands-cheatsheet.html>`_
    for many useful commands.


Using ``divio``
^^^^^^^^^^^^^^^

The ``divio`` command is used mainly to manage your local project's resources and to interact with our Control Panel.
You have already used ``divio project setup`` and ``divio project list``; you can also use it to do things like push
and pull database and media content. Try:

..  code-block:: bash

    divio project dashboard

See the :ref:`Divio CLI reference <divio-cli-ref>` for more.


Using ``docker``
^^^^^^^^^^^^^^^^

The ``docker`` command is mostly used to manage Docker processes, and Docker itself. Mostly, you'll never need to use
it, but it can be useful when you need to understand what Docker is doing on your machine, or for certain operations.
You have already used ``docker ps``. Try:

..  code-block:: bash

    docker info


Using ``docker-compose``
^^^^^^^^^^^^^^^^^^^^^^^^

The ``docker-compose`` command is used mainly to control and interact with your local project. You will mostly use it
to start the local project and open a shell in the local web container. You have already used ``docker-compose build``
and ``docker-compose up``.

Just for example, try:
