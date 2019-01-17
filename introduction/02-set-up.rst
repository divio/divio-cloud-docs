.. _tutorial-set-up:

Set up a new project
====================

..  admonition:: This tutorial assumes your project uses Django 1.11

    At the time of writing, version 1.11 is `Django's Long-Term Support release
    <https://www.djangoproject.com/download/#supported-versions>`_, and is
    guaranteed support until at least April 2020.

    If you use a different version, you will need to modify some of the code
    examples and version numbers of packages mentioned.


In this section we will create and deploy a new project in the Control Panel,
then replicate it locally.

Set up a project in the Cloud
-----------------------------

In the Divio Cloud Control Panel, create a new project.

For the purposes of this tutorial, select the following options for your
project (other options can be left on their default settings):

* *Python*: ``Python 3.x``
* *Project type*: ``Django``

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

Now let's replicate this project locally.

List your cloud projects::

    divio project list

Identify the slug of the project you created in the previous step, and use this
with the ``divio project setup`` command, for example::

    divio project setup my-tutorial-project

..  note::

    You can find the exact command, and other useful commands, by selecting
    *Local Development* from the project's menu in the Control Panel.

Various processes will unfold, taking a few minutes (see :ref:`build-process`
for a description of them).

``cd`` into the newly-created project directory, where you will find a mostly-familiar Django project.

Start the project::

    divio project up

``divio project up`` will also open the project in a web browser once it's up
and running.

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

You already know how to start your project with the ``divio`` command (``divio
project up``, above). We'll be introducing two new tools in this section:

* ``docker``
* ``docker-compose``

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

Shut it down with ``divio project stop``, the opposite of ``divio
project up``::

    ➜ divio project stop
    Stopping demoproject_web_1 ... done
    Stopping demoproject_db_1 ... done

Now ``docker ps`` should show that neither the ``web`` nor ``db`` containers
are running (see the :ref:`Docker command reference <docker-reference>` for
more information using the Docker tool).


Using ``docker-compose``
^^^^^^^^^^^^^^^^^^^^^^^^

You can also start the project with the :ref:`Docker Compose command
<docker-compose-reference>`, a command for working with projects (we will
specify that we want to bring up the ``web`` service described in the project's
:ref:`docker-compose-yml-reference` file, which also launches the ``db``
service)::

    ➜  docker-compose up web
    Starting demoproject_db_1
    Performing system checks...

    System check identified 1 issue (0 silenced).
    June 21, 2017 - 05:48:10
    Django version 1.8.18, using settings 'settings'
    Starting development server at http://0.0.0.0:80/
    Quit the server with CONTROL-C.

This is a good thing to do while developing, because it gives you the console
output in your terminal, so you can see what's going on.

When you stop it with ``CONTROL-C``, the ``web`` service will stop, but the
``db`` service will remain running. On the other hand, if you start the
project with ``docker-compose up``, then when you stop it with ``CONTROL-C``,
*both* containers will stop.

..  note::

    To make matters more complicated, under certain circumstances, the ``web``
    container may continue running after exiting from the ``docker-compose up
    web`` command. Invoking and exiting it again will usually stop it.

Now you can also run a command in a specific container, such as::

    docker-compose run --rm --service-ports web bash

which will open ``bash`` right in the ``web`` container. (``--rm`` means remove
the container when exiting; ``--service-ports`` tells it to expose the ports
listed in the ``docker-compose.yml``.) And you can run::

    python manage.py runserver 0.0.0.0:80

at the container's ``bash`` prompt as another way of running the project and
getting the output.

Use ``CONTROL-C`` to stop the runserver and ``CONTROL-D`` to exit the bash
shell and drop back into your own.
