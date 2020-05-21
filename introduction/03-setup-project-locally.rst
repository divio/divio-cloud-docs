.. _tutorial-setup-project-locally:
.. _replicate-project-locally:

Set up your project locally
========================================

In this section we will set up locally the cloud project :ref:`you created earlier <tutorial-create-project>`.

Obtain the project's slug (its unique ID) from the Dashboard:

.. image:: /images/intro-slug.png
   :alt: 'Project slug'
   :width: 400

Alternatively you can use the ``divio`` command to list your cloud project, which will show their slugs::

    divio project list


Build the project locally
-------------------------

Run the ``divio project setup`` command (for example if your project slug is ``django-project``)::

    divio project setup django-project

..  note::

    You can find other useful commands listed in `our local commands cheat sheet
    <https://docs.divio.com/en/latest/reference/local-commands-cheatsheet.html>`_.

The Divio CLI tool will build your project locally. See :ref:`build-process`
for a description of what it does.

``cd`` into the newly-created project directory, where you will find your Django project code.


Start the local project
-------------------------

Start the project by running ``docker-compose up`` in the terminal::

    ➜  docker-compose up
    Starting django-project_db_1
    Performing system checks...

    System check identified no issues (0 silenced).
    May 19, 2020 - 03:29:06
    Django version 2.2.12, using settings 'settings'
    Starting development server at http://0.0.0.0:80/
    Quit the server with CONTROL-C.

Open the project in your web browser by visiting http://0.0.0.0:8000.

(You may notice above that Django claims to be running on port 80, not port 8000. It is - but that's only *inside* the
container. The ``docker-compose.yml`` configuration file is responsible for :ref:`this port-mapping
<docker-compose-web>`.)

..  note::

    If you didn't previously log in to the cloud site before setting up the
    project locally, you'll need to add a user to the database before you can
    log in. The :ref:`Divio SSO system <divio-cloud-sso>` allows you to
    do this from the Django login page with the **Add user** option.

If you open a new terminal window and run::

    docker ps

it will show you the Docker processes that are running - you will see something like::

    ➜ docker ps
    CONTAINER ID  IMAGE              COMMAND                 CREATED         STATUS        PORTS                 NAME
    d6007edbaf32  djangoproject_web  "/tini -g -- pytho..."  17 minutes ago  Up 8 seconds  0.0.0.0:8000->80/tcp  djangoproject_web_
    27ff3e661027  postgres:9.6       "docker-entrypoint..."  17 minutes ago  Up 8 seconds  5432/tcp              djangoproject_db_

The first container is your Django project. The second is the Postgres database, running in its own Docker container.

Once you have successfully logged into the local site, try stopping the project with ``CONTROL-C``.


.. _tutorial-control:

Useful commands
----------------------------------------

So far, we have used the ``divio``, ``docker-compose`` and ``docker`` commands. It's good to have a basic familiarity
with them and what they do. As you proceed through this tutorial, you will inevitably encounter the occasional issue.
These commands will help you when this happens.


Using ``divio``
^^^^^^^^^^^^^^^

The ``divio`` command is used mainly to manage your local project's resources and to interact with our Control Panel.
You have already used it to set up your project and list your cloud projects; you can also use it to do things like
push and pull database and media content.

See the :ref:`Divio CLI reference <divio-cli-ref>` for more.


Using ``docker-compose``
^^^^^^^^^^^^^^^^^^^^^^^^

The ``docker-compose`` command is used mainly to control and interact with your local project. You will mostly use it
to start the local project and open a shell in the local web container.

Just for example, try::

    docker-compose run web python manage.py shell

which will open a Django shell in the ``web`` container.

See the :ref:`Docker Compose command reference <docker-compose-reference>`.


Using ``docker``
^^^^^^^^^^^^^^^^

The ``docker`` command is mostly used to manage Docker processes, and Docker itself.

See the :ref:`Docker command reference <docker-reference>`.
