..  This include is used by:

    * django-03-setup-project-locally.rst
    * wagtail-03-setup-project-locally.rst
    * laravel-03-setup-project-locally.rst


Local commands
----------------------------------------

So far, we have used the ``divio``, ``docker-compose`` and ``docker`` commands. It's good to have a basic familiarity
with them and what they do. As you proceed through this tutorial, you may encounter the occasional issue. These
commands will help you when this happens.

..  sidebar:: Other useful commands

    See `our local commands cheat sheet <https://docs.divio.com/en/latest/reference/local-commands-cheatsheet.html>`_
    for many more useful commands.


Using ``divio``
^^^^^^^^^^^^^^^

The ``divio`` command is used mainly to manage your local project's resources and to interact with our Control Panel.
You have already used ``divio app setup`` and ``divio app list``; you can also use it to do things like push
and pull database and media content. Try:

..  code-block:: bash

    divio app dashboard

See the :ref:`Divio CLI reference <divio-cli-ref>` for more.


Using ``docker``
^^^^^^^^^^^^^^^^

The ``docker`` command is mostly used to manage Docker processes, images and containers (rather than applications as a
whole) and Docker itself. You will rarely need to use it, but it can be useful when you need to understand what Docker
is doing on your machine, or for certain operations.

For example, if you have your project running locally (with ``docker-compose up``) open a new terminal window to run:

..  code-block:: bash

    docker ps

This will show you the Docker processes that are running - you will see something like this (note that the details will
differ depending on what you actually have running):

..  code-block:: text

    ➜ docker ps
    CONTAINER ID  IMAGE                COMMAND                 CREATED         STATUS        PORTS                 NAME
    d6007edbaf32  tutorialproject_web  "/tini -g -- pytho..."  17 minutes ago  Up 8 seconds  0.0.0.0:8000->80/tcp  tutorialproject_web_
    27ff3e661027  postgres:13.5         "docker-entrypoint..."  17 minutes ago  Up 8 seconds  5432/tcp              tutorialproject_db_

In this example, the first container is an instance of the image that you built (when deployed, a similar container
will be running in a cloud environment). The second shown here is a Postgres database, running in its own Docker
container.

You have already used ``docker ps``. Try:

..  code-block:: bash

    docker info


Using ``docker-compose``
^^^^^^^^^^^^^^^^^^^^^^^^

The ``docker-compose`` command is used mainly to control and interact with your local project. You will mostly use it
to start the local project and open a shell in the local web container. You have already used ``docker-compose build``
and ``docker-compose up``.

Just for example, try:
