.. configure-sass:

How to configure Sass CSS compilation
=====================================

`Sass <http://sass-lang.com>`_ is a popular CSS extension language, favoured by many frontend
developers.

This document explains how to implement Sass compilation in a Divio Cloud project. Although this
guide specifically deals with Sass, many of the principles it involves can be applied to other
systems.

In this example we will install, set up and run:

* Node, the server-side JavaScript application framework
* npm, the Node Package Manage
* gulp, to build the Sass CSS

..  note::

    Note that this document assumes you are working with a project that does *not* already have
    Node components set up and activated.


What we want to do
------------------

If we were doing this by hand we might run:

..  code-block:: bash

    # Activate Node Version Manager using nvm.sh (installed by default). The directory
    # $NVM_DIR is set as an environment variable by the base project:
    source $NVM_DIR/nvm.sh
    nvm install 6.10.1
    nvm alias default 6.10.1  # set a default Node version to be used in any new shell
    nvm use default  # use the default Node version now
    npm install -g npm@5.8.0  # ensure the correct version of NPM is installed
    npm install -g gulp@3.9.1
    export NODE_PATH=$NVM_DIR/versions/node/v6.10.1/lib/node_modules  # set NODE_PATH as an environment variable
    export PATH=$NVM_DIR/versions/node/v6.10.1/bin:$PATH  # Add the node directory to PATH
    # Install all required packages for building Sass (locally):
    npm install gulp@3.9.1 autoprefixer@6.7.7 gulp-clean-css@3.0.4 gulp-postcss@6.4.0 gulp-sass@3.1.0 gulp-sourcemaps@2.4.1 gutil@1.6.4
    gulp watch  # Start watching the files specified in our gulfile.js to build the CSS

However, we can use Docker to automate this for us, and also use to build some more abstraction
into the process, making it easier to maintain.


Building this into the Dockerfile
---------------------------------

See :ref:`the Divio Cloud Dockerfile reference <dockerfile-reference>` for more information on
how our ``Dockerfile`` works.


Set up the Node environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Above, we specified some version numbers for the Node environment, and we can export them here
as environment variables.

In your project's ``Dockerfile``, after the ``# <DOCKER_FROM>[...]# </DOCKER_FROM>`` section:

..  code-block:: Dockerfile

    ENV NODE_VERSION=6.10.1 NPM_VERSION=5.8.0

Using environment variables like this for version numbers allows them to be specified just once,
and re-used wherever required.

Other commands can be collected into an installation script file. This will use the
``NODE_VERSION`` and ``NPM_VERSION`` variables we set above:

..  code-block:: bash

    #!/bin/bash

    # Exit immediately in case of error
    set -e

    source $NVM_DIR/nvm.sh
    nvm install $NODE_VERSION
    nvm alias default $NODE_VERSION
    nvm use default

    npm install -g npm@"$NPM_VERSION"
    npm install -g gulp@3.9.1

The file can be added to the project repository at ``scripts/install.sh``.

Using a separate bash script for the installation commands allows us to maintain a cleaner
``Dockerfile``, and manage the installation of frontend components separately from other concerns.

Back in the ``Dockerfile``, we need to copy scripts directory to the container, and then execute
the file:

..  code-block:: Dockerfile

    ADD scripts /scripts

    RUN bash scripts/install.sh

and add the Node components to the appropriate paths:

..  code-block:: Dockerfile

    ENV NODE_PATH=$NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules \
        PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH


Install other Node packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Various other packages need to be installed locally: ``gulp``, ``autoprefixer``,
``gulp-clean-css``, ``gulp-postcss``, ``gulp-sass``, ``gulp-sourcemaps``, ``gutil``.

These should be added to a ``package.json`` in the root of the project:

..  code-block:: JSON

    {
      "name": "package",
      "private": true,
      "dependencies": {
        "autoprefixer": "^6.7.7",
        "gulp": "^3.9.1",
        "gulp-clean-css": "^3.0.4",
        "gulp-postcss": "^6.4.0",
        "gulp-sass": "^3.1.0",
        "gulp-sourcemaps": "^2.4.1",
        "gutil": "^1.6.4"
      },
      "devDependencies": {}
    }

In order to process these, you can add:

..  code-block:: Dockerfile
    :emphasize-lines: 4-6

    # <NPM>
    # package.json is put into / so that mounting /app for local
    # development does not require re-running npm install
    ENV PATH=/node_modules/.bin:$PATH
    COPY package.json /
    RUN (cd / && npm install --production && rm -rf /tmp/*)
    # </NPM>

..  note::

    It is strongly recommended to place these lines inside the ``# <NPM>[...]# </NPM>`` comments
    that exist by default in every Divio Cloud ``Dockerfile``. This is because the Divio Cloud
    Control Panel will *automatically* fill this section (if it exists) with appropriate commands
    when it discovers ``package.json`` in the project.


Run compilation of CSS at deployment time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The final part of the task is to execute ``gulp build`` to compile the CSS.

Towards the end of the ``Dockerfile``, inside the ``# <GULP>[...]# </GULP>`` section, add:

..  code-block:: Dockerfile
    :emphasize-lines: 2-3

    # <GULP>
    ENV GULP_MODE=production
    RUN gulp build
    # </GULP>

..  note::

    The ``# <GULP>[...]# </GULP>`` section exists in the ``Dockerfile`` by default. On deployment,
    the Divio Cloud Control Panel will *automatically* fill this section (if it exists) with
    appropriate commands when it discovers ``package.json`` in the project.

You will need an appropriate ``gulpfile.js`` at the root of the project too. It is beyond the scope
of this document to describe how to create a ``gulpfile``. For reference however, you may use the
file provided in our own `django CMS Boilerplate Sass
<https://github.com/divio/djangocms-boilerplate-sass/blob/master/gulpfile.js>`_. This file looks
for Sass files in ``private/sass`` and compiles them to ``/static/css``.


Building the updated project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run ``docker-compose build web`` (locally) to test the changes, or deploy them to the Test server.

In either case, the project will be started up as before, this time with compiled CSS files.

You can start the project locally with ``divio project up`` as usual. Running ``docker-compose run
--rm web gulp build`` will start a watcher that executes compilation instantly whenever a Sass file
in ``private/sass`` is changed.


Further frontend development
----------------------------

This is just an example of a particular case. It's possible to set up very extensive and
sophisticated components and processes for your project's frontend. Our `django CMS Boilerplate
Webpack <https://github.com/divio/djangocms-boilerplate-webpack>`_ is an example.

Though it's beyond the scope of this documentation to describe how to do this in detail for every
case, the basic principles are the same as in this example. If it's possible to set up, it's
possible to automate the set-up of your project's frontend components using Docker with consistent
and reliable results.


Using Boilerplates for quicker project creation
-----------------------------------------------

If you typically use the same particular frontend set-up for many sites, you should consider
packacking it up as a :ref:`Boilerplate <about-boilerplates>` that can be used at project creation
time. See :ref:`tutorial-create-boilerplate` in the tutorial section.
