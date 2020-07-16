.. _tutorial-laravel-setup-project-locally:
.. _replicate-laravel-project-locally:


..  include:: includes/03-set-up-project-locally-01.rst


Run the set-up script
---------------------

This step is required as part of the beta implementation of the PHP/Laravel project type, and will be
refined in later releases.

You'll find a script in ``divio/setup.php`` that sets up components in the project, and performs database migrations.
Run it with:

..  code-block:: bash

    docker-compose run web php /app/divio/setup.php

This takes a few minutes. Once complete, you can run your project.



Start the local project
-------------------------

Start the project by running ``docker-compose up`` in the terminal::

    ➜ docker-compose up
    tutorial-project_database_default_1 is up-to-date
    Starting tutorial-project_web_1 ... done
    Attaching to tutorial-project_database_default_1, tutorial-project_web_1
    database_default_1  | 2020-07-14 16:38:39+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 5.6.49-1debian9 started.
    [...]
    database_default_1  | 2020-07-14 16:44:42 1 [Note] Event Scheduler: Loaded 0 events
    database_default_1  | 2020-07-14 16:44:42 1 [Note] mysqld: ready for connections.
    database_default_1  | Version: '5.6.49'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
    web_1               | Laravel development server started: http://0.0.0.0:80


Open the project in your web browser by visiting http://localhost:8000.

(You may notice above that Laravel claims to be running on port 80, not port 8000. It is - but that's only *inside* the
container. The ``docker-compose.yml`` configuration file is responsible for :ref:`this port-mapping
<docker-compose-web>`.)

If you open a new terminal window and run::

    docker ps

it will show you the Docker processes that are running - you will see something like::

    ➜ docker ps
    CONTAINER ID  IMAGE                COMMAND                 CREATED         STATUS        PORTS                 NAME
    d6007edbaf32  tutorialproject_web  "/tini -g -- pytho..."  17 minutes ago  Up 8 seconds  0.0.0.0:8000->80/tcp  tutorialproject_web_
    27ff3e661027  postgres:9.6         "docker-entrypoint..."  17 minutes ago  Up 8 seconds  5432/tcp              tutorialproject_db_

The first container is your Django project. The second is the Postgres database, running in its own Docker container.

Once you have successfully logged into the local site, try stopping the project with ``CONTROL-C``.


..  include:: includes/03-set-up-project-locally-02.rst


..  code-block:: bash

    docker-compose run web composer install

This will run the ``composer install`` inside the container (in fact this is one of the command in the ``setup.php``
script you ran earlier).


..  include:: includes/03-set-up-project-locally-03.rst
