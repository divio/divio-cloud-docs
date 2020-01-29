.. _divio-cli-ref:

Divio CLI
=========

*divio-cli* is a Python-based command line application, and can be installed
via pip::

    pip install divio-cli

The `divio-cli source code <https://github.com/divio/divio-cli>`_ is available
on GitHub.

It's also available:

* in the :ref:`Divio Shell <divio-shell>`
* at the bash prompt in Divio Cloud web containers

.. _aldryn-client:

..  important::

    When using the *divio-cli* other than in a Divio Shell or web container, you will need to
    install the *aldryn-client* as well to allow the *divio-cli* to perform certain operations
    related to addons. To install::

        pip install aldryn-client

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
    Show a help message (most commands also include help messages of their own)


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
    Decrypts an encrypted backup file.

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

..  _divio-doctor:

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

    Options:

    --remote-id INTEGER
        Remote Project ID to use for project commands. Defaults to the project in the current directory using the .aldryn file.

``deploy-log``
    Returns the latest deployment log for the project's Test or Live servers.

    ``deploy-log`` takes ``test`` or ``live`` as an argument, for example::

        divio project deploy-log test

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
        * adds the addon to ``requirements.in``, as ``-e
          /app/addons-dev/tutorial-django-debug-toolbar``
        * adds any dependencies
        * runs ``docker-compose build web``.


.. _divio-project-env-vars:

``env-vars``
    Get and set :ref:`environment variables <environment-variables>`. By
    default, these operations work on the *Test* server (e.g. ``divio project
    env-vars --set SOMEKEY somevalue`` will be applied to the *Test* server,
    and will appear there).

    Note that this command applies only to the *Live* and *Test* servers, not the local server. See :ref:`Local
    environment variables <local-environment-variables>`.

    Usage: ``divio project env-vars [OPTIONS]``

    Options:

    -s, --stage TEXT
        Get data from sever (``test`` or ``live``)
    --all, --custom
        Show all or only custom (the default) variables
    --json
        Use JSON output
    --get
        Get a specific environment variable (``get VARIABLE``)
    --set
        Set a specific custom environment variable (``set VARIABLE VALUE``)
    --unset
        Unset an environment variable (``unset VARIABLE``)
    --help
        Show a help message

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

.. _divio-project-pull:

``pull``
    Pulls the database or media files from the Divio Cloud.

    Takes a required argument, ``db`` or ``media``, followed optionally by
    ``test`` or ``live`` (if not specified, defaults to ``test``), and by
    ``--remote-id <project id>`` to pull from another project.

.. _divio-project-push:

``push``
    Pushes the database or media files to the Divio Cloud.

    Takes a required argument, ``db`` or ``media``, followed optionally by
    ``test`` or ``live`` (if not specified, defaults to ``test``), and by
    ``--remote-id <project id>`` to push to another project.

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
    Updates the local project with new code changes from the Cloud, then builds it. Runs::

        git pull
        docker-compose pull
        docker-compose build
        docker-compose run web start migrate

``version``
...........

Returns version information about the *divio-cli*.
