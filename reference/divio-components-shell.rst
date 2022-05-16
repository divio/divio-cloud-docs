.. _shell:

The cloud and local shells
==========================

To interact with the environment in your application, for example to run commands using its codebase,
you can make use of a shell.

On the cloud you can :ref:`SSH into a shell instance <cloud-shell>`, provided by each running environment. Locally, you
can use the :ref:`shell <local-shell>` of the local Docker instance.

Once inside the shell, you can inspect the environment, run commands (such as ``python manage.py
migrate``). For example in a Django application It's particularly useful to be able to drop into a:

* Python console: ``python``
* Django shell: ``python manage.py shell``
* database shell: ``python manage.py dbshell``


.. _cloud-shell:

Using a cloud shell
-------------------

To open an SSH session, run::

    divio app ssh

from a local application. The default connection is to the ``test`` environment, but you can specify other environments 
by name. An instance of your web application will be spun up in a new container, and after a moment you'll be logged in 
to it as ``root``.

You can also specify a remote application with the ``--remote-id`` option.

SSH sessions are limited to 30 minutes, regardless of any activity.

You can also copy SSH connection details from the appropriate pane in the Control Panel:

.. image:: /images/environments.png
   :alt: 'Control Panel SSH icon'
   :width: 430

The command can be pasted into a terminal session on your own machine.

Note that a cloud environment must be deployed in order to reach it via SSH.


The cloud shell instance
~~~~~~~~~~~~~~~~~~~~~~~~

The container you're connected to is a brand new instance. It will not be one actually serving your
site on the web, but a new one that uses the same configuration, database and so on.

**Files** - any files you create or change on this instance will not affect those on any other
containers.

**Processes** - each session is isolated from any other extant processes (web processes, workers,
other shell sessions).

**Caches** - if your site's cache relies on the database (the default in Divio applications) then
your container will be able to make use of it, clear it and so on. However, if you're using for
example a ``locmem`` cache, it will not be available to your container.


.. _local-shell:

The local shell
---------------

Open the shell
~~~~~~~~~~~~~~~~~~~

In the application directory, run::

    docker-compose run --rm web bash

or::

    docker exec web bash  # only if the web container is already running
