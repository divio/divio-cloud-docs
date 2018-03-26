.. _install-frontend-packages:

How to add arbitrary frontend packages to a project
===================================================

The process for installing and configuring frontend packages to a project is simply a particular
case of the :ref:`process to install system-level packages <install-system-packages>` - i.e.
using ``RUN`` to execute the relevant commands in the ``Dockerfile``.

This document will use the installation of as an example, and will assume a project that uses our
base project version 3.23.


What we want to do
------------------

If we were installing these components by hand we might run:

..  code-block:: bash

    # Activate Node Version Manager using nvm.sh. Note that the directory $NVM_DIR is set as
    # an environment variable by the base project.
    source $NVM_DIR/nvm.sh

    # Install Node version 6.10.1.
    nvm install 6.10.1

    # Set a default Node version to be used in any new shell.
    nvm alias default 6.10.1

    # Use the default Node version now.
    nvm use default

    # Ensure that the correct version of Node Package Manager is globally installed.
    npm install -g npm@6.10.1

    # Install the gulp and bower packages globally
    npm install -g gulp bower

    # Set NODE_PATH as an environment variable.
    export NODE_PATH=$NVM_DIR/versions/node/v6.10.1/lib/node_modules

    # Add the node directory to PATH
    export PATH=$NVM_DIR/versions/node/v6.10.1/bin:$PATH


Using the ``Dockerfile``
------------------------

However, we need our Docker container to be set-up each time *as if* these commands had been run.

This is what the ``Dockerfile`` is for.

In fact each of these lines *could* be added as a ``RUN`` command in the ``Dockerfile``, after the:

..  code-block:: Dockerfile

    # <DOCKER_FROM>
    FROM aldryn/base-project:py3-3.23
    # </DOCKER_FROM>

section.

They'd be executed in turn when the image is created, installing and setting up the frontend
components. However, it's not a very elegant way of doing it. In practice, we'd do something a
little different in the ``Dockerfile``.


Using the ``Dockerfile`` elegantly
----------------------------------

First, we specify the version numbers as environment variables so they are easier to work with and
maintain:

..  code-block:: Dockerfile

    ENV NODE_VERSION=6.10.1 \
        NPM_VERSION=6.10.1

We'll create a new file in the project at ``scripts/install.sh``, with commands corresponding to
the steps listed above:

..  code-block:: bash

    #!/bin/bash

    # Exit immediately in case of error
    set -e

    source $NVM_DIR/nvm.sh
    nvm install $NODE_VERSION
    nvm alias default $NODE_VERSION
    nvm use default

    npm install -g npm@"$NPM_VERSION"
    npm install -g gulp bower

And back in the ``Dockerfile``, to execute this script:

..  code-block:: Dockerfile

    RUN bash scripts/install.sh

And finally, in the ``Dockerfile``:

..  code-block:: Dockerfile

    ENV NODE_PATH=$NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules \
        PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

Using a separate bash script for the installation commands allows us to maintain a cleaner
``Dockerfile``, and manage the installation of frontend components separately from other concerns.

Similarly, using environment variables for version numbers allows them to be specified just once,
and re-used wherever required.

Any scripts or processes that make use of these components will find them at runtime.

For your own frontend installation and set-up, we recommend doing something similar.

It's possible to set up very extensive and sophisticated components and processes for your
project's frontend. In short, if it's possible to set up, it's possible to automate the set-up
using Docker with consistent and reliable results.

Though it's beyond the scope of this documentation to describe how to do this in detail, the basic
principles are as outlined here.


Using Boilerplates for quicker project creation
-----------------------------------------------

If you typically use the same particular frontend set-up for many sites, you should consider
packacking it up as a :ref:`Boilerplate <about-boilerplates>` that can be used at project creation
time. See :ref:`tutorial-create-boilerplate` in the tutorial section.
