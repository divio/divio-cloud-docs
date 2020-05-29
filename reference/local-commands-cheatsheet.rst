.. _local-commands-cheatsheet:

Local commands cheatsheet
========================================================

.. _cheatsheet-project-resource-management:

Project resource management
---------------------------

Set up a project
    ``divio project setup <slug>``

Deploy Cloud server
    ``divio project deploy`` (applies to ``test`` server by default; optionally, specify ``live``)

Update local project code:
    ``divio project update`` (pulls code, updates and builds local images, runs migrations)

Build local ``web`` image (e.g. after updating ``requirements.in`` or the ``Dockerfile``)
    ``docker-compose build web``

Push/pull code
    Use ``git`` commands as appropriate.

:ref:`Pull <divio-project-pull>` or :ref:`push <divio-project-pull>`  media or database
    ``divio project pull media`` or ``divio project pull db``

    ``divio project push media`` or ``divio project push db``

    These commands apply to the ``test`` server by default; optionally, you can specify ``live``, e.g. ``divio project
    pull media live``).


Running the local server
------------------------

Start a project
    ``divio project up``, ``docker-compose up`` or ``docker-compose run --rm --service-ports web``

Stop a project
    ``divio project stop``, or exit the command with Control-C.


Working inside the containerised environment
--------------------------------------------

Run a specific command inside the web container
    ``docker-compose run --rm web <command>``, for example ``docker-compose run --rm web python manage.py shell``

Run a specific command inside the web container, exposing the ports listed in the ``Dockerfile``
    ``docker-compose run --rm --service-ports web <command>``


Docker management
-----------------

List running containers
    ``docker ps``

List all containers
    ``docker ps -a``

List images
    ``docker image ls``

Remove all stopped containers
    ``docker container prune``

Remove all unused containers and images
    ``docker system prune``
