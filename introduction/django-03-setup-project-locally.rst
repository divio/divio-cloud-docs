.. _tutorial-setup-project-locally:
.. _replicate-project-locally:


..  include:: includes/03-set-up-project-locally-01.rst


Start the local project
-------------------------

Start the project by running ``docker-compose up`` in the terminal::

    ➜  docker-compose up
    Starting tutorial-project_db_1
    Performing system checks...

    System check identified no issues (0 silenced).
    May 19, 2020 - 03:29:06
    Django version 2.2.12, using settings 'settings'
    Starting development server at http://0.0.0.0:80/
    Quit the server with CONTROL-C.

Open the project in your web browser by visiting http://localhost:8000.

(You may notice above that Django claims to be running on port 80, not port 8000. It is - but that's only *inside* the
container. The ``docker-compose.yml`` configuration file is responsible for :ref:`this port-mapping
<docker-compose-web>`.)

..  note::

    If you didn't previously log in to the cloud site before setting up the
    project locally, you'll need to add a user to the database before you can
    log in. The :ref:`Divio SSO system <divio-cloud-sso>` allows you to
    do this from the Django login page with the **Add user** option.

    Or, you could run::

        docker-compose run web manage.py createsuperuser

    See below for more on the use of ``docker-compose``.

If you open a new terminal window and run::

    docker ps

it will show you the Docker processes that are running - you will see something like::

    ➜ docker ps
    CONTAINER ID  IMAGE                COMMAND                 CREATED         STATUS        PORTS                 NAME
    d6007edbaf32  tutorialproject_web  "/tini -g -- pytho..."  17 minutes ago  Up 8 seconds  0.0.0.0:8000->80/tcp  djangoproject_web_
    27ff3e661027  postgres:9.6         "docker-entrypoint..."  17 minutes ago  Up 8 seconds  5432/tcp              djangoproject_db_

The first container is your Django project. The second is the Postgres database, running in its own Docker container.

Once you have successfully logged into the local site, try stopping the project with ``CONTROL-C``.


..  include:: includes/03-set-up-project-locally-02.rst


..  code-block:: bash

    docker-compose run web python manage.py shell

which will open a Django shell in the ``web`` container.


..  include:: includes/03-set-up-project-locally-03.rst
