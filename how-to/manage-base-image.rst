.. _manage-base-image:

How to manage a project's base image
=========================================================

Divio provides a number of `Docker base images for projects
<https://hub.docker.com/r/divio/base/tags>`_. These base images provide an underlying Linux
operating system layer, and other layers in the stack, upon which you can build your custom
application.

For example, our Python base images will include a particular version of Python, and any
system-level components required to run it.

New base images will be released with updates (for example, for newer Python releases) and other
improvements or changes. Generally, it's recommended to use the newest version of the base image
in a particular *Release Channel*.

A project's Release Channel is indicated in its Dashboard, in *Settings* > *Base Project*. Note
however that because the base image can also be specified in the repository via the ``Dockerfile``,
the manual setting will override what's indicated in the Dashboard. This document is concerned with
using the ``Dockerfile`` to manage the base image.



..  seealso::

   Reference in :ref:`dockerfile-reference-DOCKER-FROM-section`


All Divio Cloud projects are based on a customised Docker image, which uses a version of Ubuntu Linux.

If you wish to change the Python version of your project, you will need to select a different base image in the project's ``Dockerfile``.

Our base images are published at `Divio base <https://hub.docker.com/r/divio/base/tags>`.

For example, if you wish to change to Python 3.7, you could use our 0.4-py3.7-slim-stretch base image by specifying it in the ``Dockerfile``
inside the ``<DOCKER_FROM>`` section as shown below:

..  code-block:: Dockerfile
    :emphasize-lines: 2

    # <DOCKER_FROM>
    FROM divio/base:0.4-py3.7-slim-stretch
    # </DOCKER_FROM>

Note that this should be tested locally with ``docker-compose build`` before being pushed to the cloud.
