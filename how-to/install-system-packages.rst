.. _install-system-packages:

How to install system packages in a project
===========================================

..  seealso::

    * :ref:`install-python-dependencies`


All Divio projects are based on a customised Docker image, which uses a
version of Ubuntu Linux.

If your project requires a particular system package, you can include them in
the Docker image, by listing the commands required to install them - typically,
using ``RUN apt-get`` - in the ``Dockerfile``.

The commands in the ``Dockerfile`` are executed in order, so an appropriate
place to put such commands is early on, after::

    # <DOCKER_FROM>
    FROM aldryn/base-project:py3-3.23
    # </DOCKER_FROM>

and before any Python-related commands that might depend on the package.

You should include an ``apt-get update`` in the installation commands, and run
``apt-get`` with the ``-y`` ("Say *yes*") option, for example::

    RUN apt-get update
    RUN apt-get install -y wkhtmltopdf

To rebuild the docker image, installing the new packages::

    docker-compose build web

The build output will show the new ``RUN`` instructions being executed as part
of your build.

To make a quick check that the command installs what you require, without
having to rebuild the entire project, jump into a new container running
``bash`` with::

     docker-compose run --rm web bash

This container will disappear (``--rm``) when you exit.
