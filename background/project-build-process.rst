.. _build-process:

The project build process
=========================

Local builds
------------

#.  The Divio CLI clones (downloads) the project's files from its Git server.
#.  The project's ``docker-compose.yml`` file is invoked, telling Docker
    what containers need to be created, starting with the ``web`` container,
    which is built using...
#.  ...the project's ``Dockerfile``. This tells Docker how to build the
    the project's containers - Docker begins executing the commands contained
    in the file.
#.  If necessary, Docker downloads the layers from which the container image
    is built, or uses cached layers.
#.  Docker continues executing the commands, which can include copying files,
    installing packages using Pip, and running Django management commands.
#.  Docker returns to the ``docker-compose.yml``, which sets up filesystem,
    port and database access for the container, and the database container
    itself.


Cloud deployments
-----------------

A similar process unfolds on the cloud, with some differences:

* cloud projects are orchestrated by the Divio deployment system rather than a ``docker-compose.yml`` file
* the cloud does not use Docker layer caching


Notes on Docker image building
----------------------------------------------------

.. _docker-layer-caching:

Docker image/layer caching and re-use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Images and image layers are:

* not cached in cloud deployments
* cached by default in local builds


Cloud deployments
^^^^^^^^^^^^^^^^^

We don't use Docker-level layer caching on the cloud because certain cases could produce
unexpected results:

* Unpinned installation commands might install cached versions of software,
  even where the user expects a newer version.
* Commands such as ``apt-get upgrade`` in a Dockerfile could similarly
  fail to pick up new changes.
* Our clustered setup means that builds take place on different hosts. As
  Docker layer caching is local to each host, this could mean that subsequent
  builds use different versions, depending on what is in each host's cache.

When an image is built, even if nothing in the repository has changed, the image may be different from
the previously-built image. Typically, this can affect project dependencies. If a project's build instructions
specify a component, the installer (which could be ``apt``, ``pip`` or ``npm``) will typically try to install the
latest version of the component, unless a particular version is selected.

This means that if a new version has been released, the next deployment will use that - without warning, and with
possibly unexpected results. It is therefore strongly recommended to pin package versions in your project's
installation lists wherever possible to prevent this. (See also :ref:`manage-dependencies`.)


Image re-use on the cloud
^^^^^^^^^^^^^^^^^^^^^^^^^^

In some circumstances, the build process will *not* build a new image:

* If there are no new commits in the repository, and an image has been built already for the *Test*
  server, that image will be re-used for the *Live* server.
* When deploying a mirror project, the image already created for the original will be re-used.


Local builds
^^^^^^^^^^^^^^^^^

Locally, Docker **will** cache layers by default.

Local image caching can affect components that are subject to regular updates, such as Python packages installed with
``pip``. In this case, a new version of a component may have been released, but the local build will continue to use an
older version.

To turn off this behaviour, use the ``--no-cache`` option with ``docker-compose build``.
