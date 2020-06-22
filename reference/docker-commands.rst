.. _docker-commands:

Docker commands
===============

..  note::

    It is beyond the scope of this documentation to provide a complete
    reference for Docker-related commands. This page is concerned only with
    providing basic reference for these commands in the context of Divio
    projects.


.. _docker-compose-reference:

The ``docker-compose`` command
------------------------------

Docker Compose, invoked as ``docker-compose``, is used to manage :ref:`Docker
applications <application-reference>`.

The command is executed in a Docker application directory, and makes use of the
project's :ref:`docker-compose-yml-reference` file. Its general form is::

    docker-compose <command>

.. _docker-compose-build-reference:

``build``
    Builds the services (i.e. containers) listed in the ``docker-compose.yml``
    file. Optionally, takes the name of a particular service to build as an
    argument.

.. _docker-compose-rm-reference:

``rm``
    Removes (i.e. deletes) the project and its containers.


.. _docker-reference:

The ``docker`` command
----------------------

The ``docker`` command is used to manage images and containers.

Usage::

    docker <command>

``ps``
    List running Docker containers. Example::

        ➜ docker ps
        CONTAINER ID  IMAGE            COMMAND                 CREATED         STATUS        PORTS                 NAME
        d6007edbaf32  demoproject_web  "/tini -g -- pytho..."  17 minutes ago  Up 8 seconds  0.0.0.0:8000->80/tcp  demoproject_web_
        27ff3e661027  postgres:9.4     "docker-entrypoint..."  6 days ago      Up 8 seconds  5432/tcp              demoproject_db_
