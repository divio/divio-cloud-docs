.. _divio-cli-ref:

*divio-cli* reference
=====================

*divio-cli* is a Python-based command line application, and can be installed
via pip::

    pip install divio cli

The `divio-cli source code <https://github.com/divio/divio-cli>`_ is available
on GitHub.

It's also available:

* in the :ref:`Divio Shell <divio-shell>`
* at the bash prompt in Divio Cloud web containers

.. _divio-cli-command-ref:

divio-cli command reference
---------------------------

..  highlight:: bash

The *divio-cli* is invoked with the command ``divio``.

Its syntax is::

    divio [OPTIONS] COMMAND [ARGS] ...


Options
^^^^^^^

Options are:

-d, --debug
    Drop into the debugger if the command execution raises an exception.
--help
    Show a help message


Commands
^^^^^^^^

``addon``
.........

The ``addon`` command is used when in the directory of a local addon.

It take one of three commands as an argument:

``register``
    Registers an addon with the Divio Cloud addons system
``upload``
    Uploads an addon to the Divio Cloud
``validate``
    Validates basic aspects of an addon's configuration

backup
......

The ``backup`` command manages project backups.

It take one command as an argument:

``decrypt``
    Decrypts an encypted backup file.

    ``decrypt`` takes three arguments: ``KEY`` ``BACKUP`` ``DESTINATION``.

    Example::

        divio backup decrypt key backup destination

boilerplate
...........

The ``boilerplate`` command is used when in the directory of a local
boilerplate.

It take one of two commands as an argument:

``upload``
    Uploads a boilerplate to the Divio Cloud
``validate``
    Validates basic aspects of an boilerplates's configuration


doctor
......

The ``doctor`` command checks that your environment is correctly configured.

::

    ➜  divio-cloud-projects divio doctor
    Verifying your system setup
     ✓  Login
     ✓  Git
     ✓  Docker Client
     ✓  Docker Compose
     ✓  Docker Engine Connectivity
     ✓  Docker Engine Internet Connectivity
     ✓  Docker Engine DNS Connectivity


login
.....

Authorise your machine with the Divio Cloud. ``divio login`` opens your browser
at https://control.divio.com/account/desktop-app/access-token/, where you can
copy an access token to paste into the prompt.

.. _divio-cli-project-ref:

project
.......

The ``project`` command helps manage projects locally and on the Cloud.

Its general syntax is ``divio project [OPTIONS] COMMAND [ARGS]...``

Except where specifically indicated below, the ``project`` command is specific
to a particular project and must be executed within an existing project
directory.

``cheatsheet``
    Opens the project's cheatsheet page in the Control Panel.

``dashboard``
    Opens the project's Dashboard in the Control Panel.

``deploy``
    Deploys the project's Test or Live servers.

    ``deploy`` takes ``test`` or ``live`` as an argument, for example::

        divio project deploy test

.. _divio-project-develop:

``develop``
    Adds a package in development to the project.

    Usage: ``divio project develop [OPTIONS] PACKAGE``, where ``PACKAGE`` is
    the name of the addon package.

    Options:

    --no-rebuild
        Don't rebuild the Docker container

    ..  note::

        What ``divio project develop <addon>`` actually does is:

        * checks ``addons-dev`` for the named addon
        * puts the addon on the Python path
        * adds the addon to ``requirements.in``, as ``-e /app/addons-dev/tutorial-django-debug-toolbar``
        * adds any dependencies
        * runs ``docker-compose build web``.


``export``
    Exports the local database to ``local_db.sql``.

    Usage: ``divio project export db``

``import``
    Imports a database dump file into the local database.

    Usage: ``divio project import db [path]``

    If the ``path`` argument is not supplied, it will expect a file
    ``local_db.sql``.

``list``
    Lists your Divio Cloud projects.

    *Not specific to a particular project.*

``live``
    Opens the project's Live site in the browser.

``open``
    Open the local project's site in the browser.

``pull``
    Pulls the database or media files from the Divio Cloud.

    Takes a required argument, ``db`` or ``media``, followed optionally by
    ``test`` or ``live`` (if not specified, defaults to ``test``).

``push``
    Pushes the database or media files to the Divio Cloud.

    Takes a required argument, ``db`` or ``media``, followed optionally by
    ``test`` or ``live`` (if not specified, defaults to ``test``).

``setup``
    Replicates and builds a Divio Cloud project locally.

    Takes a single argument, the slug of the project.

    *Can be run outside a project folder.*

``status``
    Shows the status of the local project, shutting down its containers.

``stop``
    Stops the local project (if it is running).

``test``
    Opens the project's Test site in the browser.

``up``
    Starts up the local project.

``update``
    Updates the local project with new changes from the Cloud.

``version``
...........

Returns version information about the *divio-cli*.
