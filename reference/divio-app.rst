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

.. image:: /images/divio-app-project-list.png
   :alt: 'Divio app'
   :width: 357

Select from *All projects*, or the projects in your Personal/Organisation views. You can also
filter projects by name using the search field.

Equivalent command: ``divio project list``


.. |divio-app-toolbar-controls|  image:: /images/divio-app-toolbar-controls.png
   :alt: 'Divio app Shell launcher Help and settings'
   :width: 360

Toolbar controls |divio-app-toolbar-controls|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The toolbar allows you to open a Divio shell - a shell environment, running in Docker itself, with your keys and access to projects set up automatocally.

The other icons give you: Docker status, help, and Divio application preferences.


The local project view
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Setting up a project |divio-app-project-setup|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you select a project for the first time, you will be given the option to set it up.

.. image:: /images/divio-app-project-setup.png
   :alt: 'Project setup'
   :width: 472

When you select **Set up project**, the Divio application will clone the project's repository to the
directory specified in the the application's preferences, build it, and finally pull down its
media and database.

The command-line equivalent is ``divio project setup <project slug>``; the process is decribed
in more detail in :ref:`the project build process <build-process>`.


Managing a project
~~~~~~~~~~~~~~~~~~

.. |divio-app-project-dashboard|  image:: /images/divio-app-project-dashboard.png
   :alt: 'Divio app Dashboard launcher'
   :width: 360

.. |divio-app-project-media-db|  image:: /images/divio-app-project-media-db.png
   :alt: 'Divio app database and media controls'
   :width: 360



Return to list of projects, open the project Dashboard in the Control Panel (equivalent to: )

|divio-app-project-dashboard|

Download and upload code, media and database

|divio-app-project-media-db|


Controls for managing the local server for your project - Controls and their
command-line equivalents.

.. image:: /images/divio-app-open-local-logs-bash.png
   :alt: 'Local site controls'
   :width: 480

`Open local site`,   `Open project logs`,   `Open bash in local container`

Open the local site     ``divio project up``

Opens local server logs in a shell. Equivalent command: ``docker-compose logs
-f --tail=100``

Open a bash in the local container - local-shell ``docker-compose exec web /bin/bash``


4. Actions
^^^^^^^^^^^^


.. |divio-app-project-update-rebuild-reset| image:: /images/divio-app-project-update-rebuild-reset.png
   :alt: 'Project Update, Rebuild and Reset controls'
   :width: 180

Update, Rebuild and Reset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Controls and their command-line equivalents:

|divio-app-project-update-rebuild-reset|

**Update**   ``divio project update``

**Rebuild** ``docker-compose build web``. Note that this only rebuilds the web container. To rebuild all the project's containers, you will need to run ``docker-compose build`` in a terminal.

**Reset**   ``docker-compose rm`` to tear down the project, followed by ``divio project setup`` to rebuild it.


5. Files
^^^^^^^^^^

Manage the synchronisation of code, database and media between your local site
and the cloud Test server. Each can be downloaded or uploaded. Controls and
their command-line equivalents:

.. image:: /images/divio-app-upload-download-code-media-database.png
   :alt: 'Upload Download files'
   :width: 320

**DOWNLOAD/UPLOAD CODE** Uses ``git pull`` to update the local codebase / ``git push`` to update the Cloud project codebase.

**DOWNLOAD MEDIA / DOWNLOAD DATABASE** ``divio project pull media`` / ``divio project pull db``

**UPLOAD MEDIA / UPLOAD DATABASE** ``divio project push media`` / ``divio project push db``


As soon as the databae or the media files are transferred in either direction, they are available - there's no need to redeploy the cloud server or relaunch the local server.


.. |divio-app-project-start| image:: /images/divio-app-project-start.png
   :alt: 'Local server run controls'
   :width: 100

.. |divio-app-project-stop| image:: /images/divio-app-project-stop.png
   :alt: 'Local server run controls'
   :width: 100

6. Run controls |divio-app-project-start|  /  |divio-app-project-stop|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manage the state of the local server. Controls and their command-line
equivalents:

**START**  ``docker-compose up``

**STOP**  ``docker-compose stop``

.. |divio-app-open-cloud-dashboard| image:: /images/divio-app-open-cloud-dashboard.png
   :alt: 'Open Dashboard'
   :width: 50

7. Could Dashboard
^^^^^^^^^^^^^^^^^^^^^

|divio-app-open-cloud-dashboard|

The Divio app communicates with the Control Panel to provide basic management
of your Test and Live servers. Command-line equivalent is ``divio project dashboard``


8. File synchronisation
^^^^^^^^^^^^^^^^^^^^^^^^

(Must be enabled in the Divio app's settings). When active, synchronises
frontend file (HTML templates, CSS and JavaScript) changes between the local
and test servers. This may be useful to frontend developers, for quick changes.


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

The Divio Shell is a pre-configured shell environment for interacting with
local Divio projects. It's launched with the |divio-shell| button in the bottom
left corner of the Divio app, and drops you in a bash prompt, in your Divio
Cloud workspace directory.

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
