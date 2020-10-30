.. _divio-cli-ref:

Divio CLI
=========

*divio-cli* is a Python-based command line application, and can be installed
via pip::

    pip install divio-cli

The `divio-cli source code <https://github.com/divio/divio-cli>`_ is available
on GitHub.

.. click:: divio_cli.cli:cli
   :prog: divio-cli
   :nested: full

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
    Registers an addon with the Divio addons system
``upload``
    Uploads an addon to Divio
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
    Uploads a boilerplate to Divio
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

Authorise your machine with Divio. ``divio login`` opens your browser
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



.. _aldryn-client:

..  note::

    When using the *divio-cli* other than in a Divio Shell or web container, you will need to
    install the *aldryn-client* as well to allow the *divio-cli* to perform certain operations
    related to addons. To install::

        pip install aldryn-client
