.. _local-commands-cheatsheet:

Local commands cheatsheet
========================================================

Project resource management
---------------------------

Set up a project
    ``divio project setup <slug>``

Deploy test server
    ``divio project deploy`` (applies to ``test`` server by default; optionally, specify ``live``)

Update local project code:
    ``divio project update`` (pulls code, updates and builds local images, runs migrations)

Build local ``web`` image (e.g. after updating ``requirements.in``)
    ``docker-compose build web``

Push/pull code
    use ``git`` ``add``/``commit``/``push``/``pull`` commands as appropriate

Push/pull media
    ``divio project push media``/``divio project pull media`` (applies to ``test`` server by default; optionally,
    specify ``live``)

Push/pull database
    ``divio project push db``/``divio project pull db`` (applies to ``test`` server by default; optionally, specify
    ``live``)


Running the local server
------------------------

Start a project
    ``divio project up``, ``docker-compose up`` or ``docker-compose run --rm --service-ports web``

Stop a project
    ``divio project stop``, or exit the command with Control-C.


Working inside the containerised environment
--------------------------------------------

Run a specific command inside the web container
    ``docker-compose run --rm web <command>``

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
