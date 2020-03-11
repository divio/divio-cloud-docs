.. _shell:

The Cloud and local shells
==========================

To interact with the environment in your project, for example to run commands using its code-base,
you can make use of a shell.

On the Cloud you can :ref:`SSH into a Cloud shell instance <cloud-shell>` (available on Managed
Cloud projects only). Locally, you can use the :ref:`local Shell <local-shell>`.

Once inside the shell, you can inspect the environment, run commands (such as ``python manage.py
migrate``). It's particularly useful to be able to drop into a:

* Python console: ``python``
* Django shell: ``python manage.py shell``
* database shell: ``python manage.py dbshell``

..  important::

    The Cloud and local shells described here are not to be confused with the :ref:`Divio Shell
    <divio-shell>`.

    The Divio Shell is a convenient environment on your own computer, configured for interaction
    with your Divio Cloud account and projects, and the local development environment.

    The Cloud and local shells will provide you with terminal access inside a running project.


.. _cloud-shell:

Using a Cloud shell
-------------------

The Cloud shell is only available for Managed Cloud projects.

Your Cloud server must be deployed in order to reach it via SSH. You can copy SSH connection
details from the appropriate server pane in the Control Panel:

.. image:: /images/control-panel-open-shell.png
   :alt: 'Control Panel SSH icon'
   :width: 430

The command can be pasted into a terminal session on your own machine. An instance of your web
application will be spun up in a new container, and after a moment you'll be logged in to it as
``root``.

SSH sessions are limited to 30 minutes, regardless of any activity.


The Cloud shell instance
~~~~~~~~~~~~~~~~~~~~~~~~

The container you're connected to is a brand new instance. It will not be one actually serving your
site on the web, but a new one that uses the same configuration, database and so on.

**Files** - any files you create or change on this instance will not affect those on any other
containers.

**Processes** - each session is isolated from any other extant processes (web processes, workers,
other shell sessions).

**Caches** - if your site's cache relies on the database (the Divio Cloud Projects default) then
your container will be able to make use of it, clear it and so on. However, if you're using for
example a ``locmem`` cache, it will not be available to your container.


.. _local-shell:

The local shell
---------------

Open the shell
~~~~~~~~~~~~~~~~~~~

The Divio app provides a convenient short-cut in its toolbar:

.. image:: /images/divio-app-controls-toolbar.png
   :alt: 'Divio app Shell launcher Help and settings'
   :width: 360

Alternatively, you can use the command-line. In the project directory, run::

    docker exec web bash  # if the web container is already running

or::

    docker-compose run --rm web bash  # if you need to start the container too

