.. _local-commands-cheatsheet:

Local commands cheatsheet
========================================================

.. _cheatsheet-project-resource-management:

Project resource management
---------------------------

Set up a project
    ``divio app setup <slug>``

Deploy Cloud server
    ``divio app deploy`` (applies to ``test`` server by default; optionally, specify ``live``)

Build local ``web`` image (e.g. after updating ``requirements.in`` or the ``Dockerfile``)
    ``docker-compose build web``

Push/pull code
    Use ``git`` commands as appropriate.

Pull or push media or database
    ``divio app pull media`` or ``divio app pull db``

    ``divio app push media`` or ``divio app push db``

    These commands apply to the ``test`` server by default; optionally, you can specify ``live``, e.g. ``divio app
    pull media live``).

Manage environment variables
     ``divio app env-vars`` - get custom values

     ``divio app env-vars --all`` - get all values

     ``divio app env-vars -s qa`` - get the values from the environment named *qa*

     ``divio app env-vars --set TEST myvalue`` - set the variable ``TEST`` to ``myvalue``



Running the local server
------------------------

Start a project
    ``divio app up``, ``docker-compose up`` or ``docker-compose run --rm --service-ports web``

Stop a project
    ``divio app stop``, or exit the command with Control-C.


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
