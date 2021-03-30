:orphan:

.. meta::
   :description:
       This guide explains step-by-step how to deploy a Gatsby application with Docker, in accordance with
       Twelve-factor principles.
   :keywords: Docker, Gatsby


How to deploy a Gatsby application on Divio
===========================================================================================

`Gatsby <https://www.gatsbyjs.com>`_ is very popular React-based open-source framework for creating websites and apps.

..  include:: /how-to/includes/deploy-common-intro.rst

The steps outlined here assume that you have a working Gatsby project.

However, if you need a basic working example, and already have a suitable version of Node installed, you can do:

..  code-block:: bash

    npm install -g gatsby-cli
    gatsby new hello-world https://github.com/gatsbyjs/gatsby-starter-hello-world

and then in the new directory:

..  code-block:: bash

    gatsby develop -H 0.0.0.0 -p 8000

to see it running locally.

..  include:: /how-to/includes/deploy-common-prerequisites.rst

.. _deploy-gatsby-dockerfile:

..  include:: /how-to/includes/deploy-common-dockerfile.rst

For a Gatsby application, you can use:

..  code-block:: Dockerfile

    FROM node:14.15.1-alpine

``14.15.1-alpine`` is the name of the Docker *base image*. We cannot advise on what base image you should use; you'll
need to use one that is in-line with your application's needs. It's good practice to use a specific base image - for
example ``node:14.15.1-alpine`` above (rather than say just ``node:14``).

..  seealso::

    * :ref:`manage-base-image-choosing`
    * `Divio base images on Docker Hub <https://hub.docker.com/r/divio/base/tags?page=1&ordering=last_updated>`_

..  include:: /how-to/includes/deploy-common-dockerfile-system-dependencies.rst

In this case, we can use APK since we are using an Alpine Linux base image:

..  code-block:: Dockerfile

    RUN apk add --no-cache \
      make g++ && \
      apk add vips-dev fftw-dev --update-cache \
      && rm -fR /var/cache/apk/*

..  include:: /how-to/includes/deploy-common-dockerfile-working-directory.rst

..  include:: /how-to/includes/deploy-common-dockerfile-application-dependencies.rst

Assuming you're using a ``package.json``/``package-lock.json``:

..  code-block:: Dockerfile

    RUN npm install
    RUN npm install -g gatsby-cli

It's important to pin dependencies as firmly as possible.

..  include:: /how-to/includes/deploy-common-dockerfile-file-building.rst

For Gatsby, add:

..  code-block:: Dockerfile

    RUN gatsby build

.. _deploy-gatsby-dockerfile-cmd:

..  include:: /how-to/includes/deploy-common-dockerfile-cmd.rst

A suitable command for Gatsby would be:

..  code-block:: Dockerfile

    CMD gatsby serve --port 80 --host 0.0.0.0

However if your ``package.json`` already includes a suitable entry in its ``scripts`` section, you could also make use
of that, so for example:

..  code-block::

    "scripts": {
      ...
      "deploy": "gatsby serve --port 80 --host 0.0.0.0"
    },

and in the ``Dockerfile`` instead use:

..  code-block:: Dockerfile

    CMD npm run deploy

..  include:: /how-to/includes/deploy-common-cmd-admonition.rst

..  include:: /how-to/includes/deploy-common-dockerfile-access-services.rst

.. _deploy-gatsby-configuration:

..  include:: /how-to/includes/deploy-common-configuration-services.rst

..  include:: /how-to/includes/deploy-common-helper-modules.rst

Rather than re-inventing the wheel when it comes to reading and applying configuration from environment variables,
we advise to make use of existing helper modules that have solved this problem already.

..  include:: /how-to/includes/deploy-common-settings-security.rst

..  include:: /how-to/includes/deploy-common-settings-database.rst

..  include:: /how-to/includes/deploy-common-settings-static.rst

..  include:: /how-to/includes/deploy-common-settings-media.rst

See the Django guide for :ref:`a concrete example <deploy-django-media>`.

..  include:: /how-to/includes/deploy-common-settings-media-admonition.rst

..  include:: /how-to/includes/deploy-common-settings-other.rst

.. _deploy-gatsby-docker-compose:

..  include:: /how-to/includes/deploy-common-compose.rst

..  code-block:: yaml
    :emphasize-lines: 13, 17, 21-22, 24-

    version: "2.4"
    services:
      web:
        # the application's web service (container) will use an image based on our Dockerfile
        build: "."
        # map the internal port 80 to port 8000 on the host
        ports:
          - "8000:80"
        # map the host directory to app (which allows us to see and edit files inside the container)
        volumes:
        # uncomment if you prefer to perform node install/gatsby build operations on the host
        # system - see the Divio Gatsby Quickstart how-to guide for an explanation
        #   - ".:/app:rw"
          - "./data:/data:rw"
        # the default command to run whenever the container is launched - this can be different from
        # the command built into the image
        command: gatsby develop --port 80 --host 0.0.0.0
        env_file: .env-local
        # if required, the URL 'postgres' or 'mysql' will point to the application's db service
        # - but remove the entire links section if not required
        # links:
        #   - "database_default"

      # # this entire section can be removed if you're not using a database
      #
      # database_default:
      #   # Select one of the following db configurations for the database
      #   image: postgres:9.6-alpine
      #   environment:
      #     POSTGRES_DB: "db"
      #     POSTGRES_HOST_AUTH_METHOD: "trust"
      #     SERVICE_MANAGER: "fsm-postgres"
      #   volumes:
      #     - ".:/app:rw"
      #
      #   image: mysql:5.7
      #   environment:
      #     MYSQL_DATABASE: "db"
      #     MYSQL_ALLOW_EMPTY_PASSWORD: "yes"
      #     SERVICE_MANAGER: "fsm-mysql"
      #   volumes:
      #     - ".:/app:rw"
      #     - "./data/db:/var/lib/mysql"
      #   healthcheck:
      #       test: "/usr/bin/mysql --user=root -h 127.0.0.1 --execute \"SHOW DATABASES;\""
      #       interval: 2s
      #       timeout: 20s
      #       retries: 10


.. _deploy-gatsby-env-local:

..  include:: /how-to/includes/deploy-common-compose-env-local.rst

..  code-block:: text
    :emphasize-lines: 2-3

    # Select one of the following for the database
    DATABASE_URL=postgres://postgres@database_default:5432/db
    DATABASE_URL=mysql://root@database_default:3306/db

    # Storage will use local file storage in the data directory
    DEFAULT_STORAGE_DSN=file:///data/media/?url=%2Fmedia%2F

In cloud environments, we provide a number of useful variables. If your application needs to make use of them (see a
:ref:`Django example <deploy-django-security>`) you should provide them for local use too. For example:

..  include:: /how-to/includes/deploy-common-compose-summary.rst

..  include:: /how-to/includes/deploy-common-buildrun-build.rst

Building on the host as an option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you uncomment the:

..  code-block:: YAML

    # - ".:/app:rw"

entry in the ``web:volumes`` section of ``docker-compose.yml``, the entire ``/app`` directory will be overridden by the
project files from the host. This can be useful for development. However, you will now need to run the commands ``npm
install`` and ``gatsby build`` on the host as well in order to regenerate the files so that the container sees them.

..  include:: /how-to/includes/deploy-common-buildrun-run.rst


..  include:: /how-to/includes/deploy-common-git.rst

For a basic project you'll probably need at least:

..  code-block:: text

    # used by the Divio CLI
    .divio
    /data.tar.gz

    # for local file storage
    /data


..  include:: /how-to/includes/deploy-common-deploy.rst
