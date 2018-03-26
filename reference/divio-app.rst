.. _divio-app:

The Divio application
=====================

The Divio app is a GUI application for interacting with local projects and
the Divio Cloud.

It also sets up :ref:`the Divio Shell <divio-shell>`.


Controls
--------

Most of the controls in the Divio app correspond to :ref:`divio-cli-ref` or
:ref:`docker-compose <docker-compose-reference>` commands.

.. image:: /images/divio-app-annotated.png
   :alt: 'Divio app'
   :width: 720


1. The Project list
^^^^^^^^^^^^^^^^^^^

Also shows the running project, if any.

Equivalent command: ``divio project list``


2.  Organisation list
^^^^^^^^^^^^^^^^^^^^^

Switch between projects lists for multiple organisations.


3.  General application controls |divio-app-general-controls|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. |divio-app-general-controls| image:: /images/divio-app-general-controls.png
   :alt: 'Divio app general controls'
   :width: 205

Status, refresh, account settings


.. |divio-shell| image:: /images/divio-shell.png
   :alt: 'Divio Shell'
   :width: 108

4. Divio Shell launcher |divio-shell|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`The Divio Shell <divio-shell>`, below.


.. |divio-app-local-controls| image:: /images/divio-app-local-controls.png
   :alt: 'Local site controls'
   :width: 292

5. The local project pane |divio-app-local-controls|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Controls for managing the local server for your project. Controls and their
command-line equivalents:

Open a bash shell in the local container
    ``docker-compose exec web /bin/bash``
Open the local site
    ``divio project up``


.. |divio-app-setup-controls| image:: /images/divio-app-setup-controls.png
   :alt: 'Local site controls'
   :width: 285

6. Actions |divio-app-setup-controls|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Setup menu offers different options for managing the local project as a
whole. Controls and their command-line equivalents:

Setup
    ``divio project setup <project slug>``
Update
    ``divio project update``
Rebuild
    ``docker-compose build web``. Note that this only rebuilds the web
    container. To rebuild all the project's containers, you will need to run
    ``docker-compose build`` in a terminal.
Reset
    ``docker-compose rm`` to tear down the project, followed by ``divio project
    setup`` to rebuild it.


.. |divio-app-file-controls| image:: /images/divio-app-file-controls.png
   :alt: 'Local file controls'
   :width: 285

7. Files |divio-app-file-controls|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manage the syncronisation of code, database and media between your local site
and the cloud Test server. Each can be downloaded or uploaded. Controls and
their command-line equivalents:

Download/Upload
    Uses ``git pull`` to update the local codebase/``git push`` to update the Cloud project
    codebase.
Media Download/Upload
    ``divio project pull media db``/``divio project push media``

    As soon as the media files are transferred in either direction, they are
    available - there's no need to redeploy the cloud server or relaunch the
    local server.
Database Download/Uploading
    ``divio project pull db``/``divio project push db``

    As soon as the database is transferred in either direction, it is available
    - there's no need to redeploy the cloud server or relaunch the local server.


.. |divio-app-run-controls| image:: /images/divio-app-run-controls.png
   :alt: 'Local server run controls'
   :width: 280

8. Run controls |divio-app-run-controls|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manage the state of the local server. Controls and their command-line
equivalents:

Start
    ``docker-compose up``
Stop
    ``docker-compose stop``


.. |divio-app-server-logs| image:: /images/divio-app-server-logs.png
   :alt: 'Local server logs'
   :width: 223

9. Logs |divio-app-server-logs|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Opens local server logs in a shell. Equivalent command: ``docker-compose logs
-f --tail=100``


.. |divio-app-test-controls| image:: /images/divio-app-test-controls.png
   :alt: 'Test server controls'
   :width: 285

10. Test server pane |divio-app-test-controls|
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Divio app communicates with the Control Panel to provide basic management
of your Test server. Controls and their command-line equivalents:

Open Cloud project Dashboard
    ``divio project dashboard``
Open Test site
    ``divio project test``

.. |divio-app-test-deploy| image:: /images/divio-app-test-deploy.png
   :alt: 'Deploy Test server'
   :width: 296

There is also a Deploy Test site button |divio-app-test-deploy|. This runs:
``divio project deploy test``


11. File synchronisation
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

    The Divio Shell and the local container's bash shell are quite different.
    The Divio Shell is for interacting with your Divio projects. The local
    container bash shell is *inside* an instance of a particular project,
    allowing you to interact with its program code and operations.


Creating the shell
^^^^^^^^^^^^^^^^^^

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

