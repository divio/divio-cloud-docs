The ``Dockerfile`` - define how to build the application
----------------------------------------------------------------------

The application needs a ``Dockerfile`` at the root of repository, that defines how to build the
application. The ``Dockerfile`` starts by importing a base image, for example:

..  code-block:: Dockerfile

    FROM python:3.8

Here, ``python:3.8`` is the name of the Docker *base image*. We cannot advise on what base image you should use;
you'll need to use one that is in-line with your application's needs. However, once you have a working set-up, it's
good practice to move to a more specific base image - for example ``python:3.8.1-slim-buster``.

..  seealso::

    * :ref:`manage-base-image-choosing`
    * `Divio base images on Docker Hub <https://hub.docker.com/r/divio/base/tags?page=1&ordering=last_updated>`_

We recommend setting up a working directory early on in the ``Dockerfile`` before you need to write any files, for
example:

..  code-block:: Dockerfile

    # set the working directory
    WORKDIR /app
    # copy the repository files to it
    COPY . /app
