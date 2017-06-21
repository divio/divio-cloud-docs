.. _divio-app:

The Divio application
=====================

The Divio app is a GUI application for interacting with local projects and
the Divio Cloud.

It also sets up :ref:`the Divio Shell <divio-shell>`.

.. image:: /images/divio-app.png
   :alt: 'Divio app'
   :width: 720


Installation
------------

When first run, the Divio app will:

*   download Docker
*   install Docker
*   launch it
*   set up a local Docker image that provides a Bash shell interface for issuing
    ``divio`` commands, even if the Divio CLI has not been installed globally


Controls
--------

Most of the controls in the Divio app correspond to :ref:`divio-cli-ref` or
:ref:`docker-compose-reference` commands. This is a list of the controls and
the corresponding commands:

The Project list
    ``divio project list``
Setup
    ``divio project setup <project slug>``
Update
    ``divio project update``
Rebuild
    ``docker-compose build``
Reset
    ``docker-compose rm`` to tear down the project, followed by ``divio project
    setup`` to rebuild it.
Download
    Uses ``git pull`` to update the local codebase.
Media Download
    ``divio project pull media db``
Database Download
    ``divio project pull db``
Upload
    Uses ``git push`` to update the Cloud project codebase.
Upload Media
    ``divio project push media``
Upload Database
    ``divio project push db``
Start
    ``docker-compose up``
Stop
    ``docker-compose stop``
Open local site (eye icon)
    ``divio project up``
Open bash in local container
    ``docker-compose exec web /bin/bash``
Show server logs
    ``docker-compose logs -f --tail=100``

Some other controls in the Divio app also match command-line operations, though
they are in fact executed via APIs on the Control Panel:

Project Dashboard
    ``docker-compose logs -f --tail=100``
Open Test site
    ``divio project test``
Deploy
    ``divio project deploy test``


.. _divio-shell:

The Divio Shell
---------------

.. |divio-shell| image:: /images/divio-shell.png
   :alt: 'Divio Shell'
   :width: 108

The Divio Shell is a pre-configured shell environment for interacting with
local Divio projects. It's launched with the |divio-shell| button in the bottom
left corner of the Divio app.

The Divio app creates the shell by running a sequence of commands, expanded
here for clarification:

..  todo:: Explain what this means.

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

The shell drops you in a bash prompt, in your Divio Cloud workspace directory.
