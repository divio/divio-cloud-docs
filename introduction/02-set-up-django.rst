.. _tutorial-aldryn-django-set-up:

Set up a new Django/Aldryn project
==================================

..  admonition:: This tutorial assumes your project uses Django 1.11

    At the time of writing, version 1.11 is `Django's Long-Term Support release
    <https://www.djangoproject.com/download/#supported-versions>`_, and is
    guaranteed support until at least April 2020.

    If you use a different version, you will need to modify some of the code
    examples and version numbers of packages mentioned.

This part of the tutorial will introduce you to the Divio development/deployment workflow using Aldryn and a Django
project as an example.

In this page we will create and deploy a new project in the Control Panel, then replicate it locally.

If you have not already done so, you will need to :ref:`create your Divio account and set up the local development
environment <tutorial-installation>`.


Create a new Aldyn Django project
---------------------------------

On the Control Panel, create a new project selecting:

* *Python*: ``Python 3.x``
* *Project type*: ``Django``

Other options can be left on their default settings.


Deploy the project
------------------

Once the project has been created, deploy the Test server, and then login to
the admin.

..  note::

    By logging in, you will add your :ref:`divio-cloud-sso` user to the
    project's database, and will be able to log in to the site locally without
    having to add the new user to the database manually.

You'll see a familiar Django admin for a new site.


.. _replicate-project-locally:

Replicate it locally
--------------------

List your cloud projects::

   divio project list

Identify the slug of the project you created in the previous step, and use this with the ``divio project setup``
command, for example::

   divio project setup my-tutorial-project

Various processes will unfold, taking a few minutes (see :ref:`build-process` for a description of them).


.. _local_project_start:

Start the local project
-----------------------

``cd`` into the newly-created project directory, where you will find a mostly-familiar Django project.

Start the project with ``docker-compose up``::

    ➜  docker-compose up
    Starting demoproject_db_1
    Performing system checks...

    System check identified 1 issue (0 silenced).
    June 21, 2017 - 05:48:10
    Django version 1.8.18, using settings 'settings'
    Starting development server at http://0.0.0.0:80/
    Quit the server with CONTROL-C.

Once up and running, you will be able to open the project in a web browser on port 8000 (i.e. at ``localhost:8000``).

..  note::

    If you didn't previously log in to the Cloud site before setting up the
    project locally, you'll need to add a user to the database before you can
    log in. The :ref:`Divio Cloud SSO system <divio-cloud-sso>` allows you to
    do this from the Django login page.


.. _tutorial-control:

Control your project and see its console
----------------------------------------

As you proceed through this tutorial, you will inevitably encounter the
occasional issue. There are some commands that will help you when this happens.

As well as ``divio`` and ``docker-compose`` commands as used above, you will sometimes need to use ``docker``.

This may seem a complex combination of commands, but through practice you will
start to understand when and how to use each one. **Try them now to become
familiar with them.**


Using ``docker``
^^^^^^^^^^^^^^^^

Check what Docker processes are running::

    ➜ docker ps
    CONTAINER ID  IMAGE            COMMAND                 CREATED         STATUS        PORTS                 NAME
    d6007edbaf32  demoproject_web  "/tini -g -- pytho..."  17 minutes ago  Up 8 seconds  0.0.0.0:8000->80/tcp  demoproject_web_
    27ff3e661027  postgres:9.4     "docker-entrypoint..."  6 days ago      Up 8 seconds  5432/tcp              demoproject_db_

You can kill a process with ``docker kill <process id>`` - though this isn't a very graceful way of stopping something.

See the :ref:`Docker command reference <docker-reference>` for more information using the Docker tool.


Using ``docker-compose``
^^^^^^^^^^^^^^^^^^^^^^^^

``docker-compose up`` brings up the project, using the ``command`` listed for the ``web`` service in the
``docke-compose.yml`` file.

You can also bring up a container and run a specific command in it, for example::

    docker-compose run --rm --service-ports web bash

which will open ``bash`` right in the ``web`` container. (``--rm`` means remove
the container when exiting; ``--service-ports`` tells it to expose the ports
listed in the ``docker-compose.yml``.) And you can run::

    python manage.py runserver 0.0.0.0:80

at the container's ``bash`` prompt as another way of running the project and
getting the output.

Use ``CONTROL-C`` to stop the runserver and ``CONTROL-D`` to exit the bash
shell and drop back into your own.
