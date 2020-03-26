.. _divio-app:

The Divio application
=====================

The Divio app is a GUI application for interacting with local projects and
the Divio Cloud. It also sets up :ref:`the Divio Shell <divio-shell>`.


Controls
--------

Most of the controls in the Divio app correspond to :ref:`divio-cli-ref` or
:ref:`docker-compose <docker-compose-reference>` commands.


Project list
^^^^^^^^^^^^^^^^^^^

The Divio application opens with a list of the projects available to you.

.. image:: /images/divio-app-project-list.png
   :alt: 'Divio app'
   :width: 472

Select from *All projects*, or the projects in your Personal/Organisation views. You can also
filter projects by name using the search field. The equivalent command is ``divio project list``.

Select a project to see its status in your local environment.


Toolbar controls
^^^^^^^^^^^^^^^^

The toolbar at the bottom of the application interface is always available and provides some useful
controls:

.. image:: /images/divio-app-controls-toolbar.png
   :alt: 'Divio app Shell launcher Help and settings'
   :width: 360

**Open shell** will open a shell environment, running in Docker itself, with your keys and access
to projects set up automatically.

The other icons give you:

* Docker status
* help options
* Divio application preferences


Setting up a project
^^^^^^^^^^^^^^^^^^^^

When you select a project for the first time, you will be given the option to set it up.

.. image:: /images/divio-app-project-setup.png
   :alt: 'Project setup'
   :width: 472

When you select **Set up project**, the Divio application will clone the project's repository to the
directory specified in the the application's preferences, build it, and finally pull down its
media and database. While it does this, it will also display the local build log.

.. image:: /images/divio-app-project-setup-process.png
   :alt: 'Project setup process'
   :width: 472

The command-line equivalent is ``divio project setup <project slug>``; the process is described in
more detail in :ref:`the project build process <build-process>`. The process can take a few minutes.

Once successfully set up, the application will show more information and options for managing the
project.

.. image:: /images/divio-app-project-controls.png
   :alt: 'Divio app Dashboard launcher'
   :width: 472


Managing a project
^^^^^^^^^^^^^^^^^^

Project list/open Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /images/divio-app-project-controls-back-launch.png
   :alt: 'Divio app Dashboard launcher'
   :width: 472

Return to list of projects; open the project Dashboard in the Control Panel (equivalent to ``divio
project dashboard``).


Download/upload
~~~~~~~~~~~~~~~

.. image:: /images/divio-app-project-controls-download-upload.png
   :alt: 'Divio app database and media controls'
   :width: 472

**Download** and **Upload** controls for:

* code (equivalent: using ``git`` commands to interact with the repository)
* media (equivalent: using ``divio project push media`` and ``divio project push media`` commands)
* database (equivalent: using ``divio project push db`` and ``divio project push db`` commands)


Open local files
~~~~~~~~~~~~~~~~

.. image:: /images/divio-app-project-controls-local-files.png
   :alt: 'Divio app open project directory'
   :width: 472

Open the local project directory for access to the files.


Start/stop
~~~~~~~~~~

.. image:: /images/divio-app-project-controls-start-stop.png
   :alt: 'Divio app open project directory'
   :width: 472

**Start** to launch the local project (or **Stop** if it is already running).


Options when running
~~~~~~~~~~~~~~~~~~~~

The other options are only available when the project is running locally:

.. image:: /images/divio-app-project-controls-running-options.png
   :alt: 'Divio app options when running'
   :width: 472

Respectively, they will:

* open the local site in your browser
* open a console displaying the site runtime logs in a Divio shell; equivalent to
  ``docker-compose logs -f --tail=100``
* open a shell inside the local site's ``web`` container; equivalent to ``docker-compose
  exec web /bin/bash``
* present additional options for managing the Docker build:

  * **Update** - equivalent to ``divio project update`` (pulls latest Git commits, rebuilds)
  * **Rebuild** -  equivalent to ``docker-compose build web``
  * **Reset** - equivalent to ``docker-compose rm`` to tear down the project, followed by ``divio project setup`` to rebuild it.


First run
---------

When first run, the Divio app will:

*   download Docker
*   install Docker
*   launch it
*   set up a local Docker image that provides a Bash shell interface for issuing
    ``divio`` commands, even if the Divio CLI has not been installed globally


.. _divio-shell:

The Divio Shell
---------------

The Divio Shell is a pre-configured shell environment for interacting with local Divio projects.
It's launched with the **open shell** button in the toolbar of the Divio app, and drops you in a
bash prompt, in your Divio Cloud workspace directory.

The Divio Shell is configured with the SSH keys required to give you access to
our Cloud servers. You don't have to use the Divio Shell (you can use an
ordinary session in your terminal) but in that case you will need to :ref:`set
up keys yourself <add-public-key>`.

..  important::

    The Divio Shell and the :ref:`local container's bash shell <local-shell>` are quite different.

    * The Divio Shell is for interacting with your Divio projects.
    * The :ref:`local container bash shell <local-shell>` is *inside* an instance of a particular
      project, allowing you to interact with its program code and operations.


Creating the Divio shell
^^^^^^^^^^^^^^^^^^^^^^^^

The Divio app creates the shell by running a sequence of commands, expanded
here for clarification:

..  code-block:: bash

    # clear the terminal window
    clear
    # set the path for this shell
    PATH=$HOME/.local/bin:/usr/local/bin:$PATH
    # clears the DOCKER_HOST environment variable, in case something else has set it
    unset DOCKER_HOST
    # runs a docker command in a new container, with interactive TTY access, removing it on exit
    docker run -it --rm \
        # ... mounting  these volumes in the container:
        -v '/var/run/docker.sock:/var/run/docker.sock:rw' \
        -v '/Users/daniele/.netrc:/home/divio/.netrc:rw' \
        -v '/Users/daniele/.aldryn:/home/divio/.aldryn:rw' \
        -v '/Users/daniele/divio-cloud-projects:/Users/daniele/divio-cloud-projects:rw'
        # ... using the image:
        divio/divio-app-toolbox:daniele-0.10.5-daniele.procida_divio.ch
        # ... and in the new container, run the following commands:
        cd /Users/daniele/divio-cloud-projects
        divio doctor
        bash
