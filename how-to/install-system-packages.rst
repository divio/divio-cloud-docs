.. _install-system-packages:

How to install system packages in a project
===========================================

..  seealso::

    * :ref:`install-python-dependencies`

All Divio projects are based on a ``Dockerfile`` that starts with base image that includes Linux.

If your project requires particular system packages, you can include them in
the Docker image, by listing the commands required to install them - typically,
using ``RUN apt-get`` - in the ``Dockerfile``.

The commands in the ``Dockerfile`` are executed in order, so an appropriate
place to put such commands is early on, after ``FROM`` - for example, after:

..  code-block:: dockerfile

    FROM divio/base:0.4-py3.7-slim-stretch

and before any other commands that might depend on the package.

You should include an ``apt-get update`` in the installation commands, and run
``apt-get`` with the ``-y`` ("Say *yes*") option, for example:

..  code-block:: dockerfile

    RUN apt-get update
    RUN apt-get install -y postgres-client

to install the ``psql`` Postgres client.

To rebuild the docker image, installing the new packages:

..  code-block:: bash

    docker-compose build web

The build output will show the new ``RUN`` instructions being executed as part
of your build.
