.. _build-process:

The project deployment process
==============================

Deployment steps
-----------------

#. The Control Panel checks that required services (such as the database) are available.
#. The project's Git repository is checked out.
#. An image is built, using the instructions in the ``Dockerfile``.
#. A container is deployed from the image.
#. Any migration commands (post-build instructions) defined by the project are executed.
#. Additional containers are deployed according to the project's configuration.
#. The Control Panel tests that the application is responding.


Zero-downtime cloud deployments
-------------------------------

If all of the steps above are successful, then the deployment is marked as successful, and requests will be routed to
the new containers, and the old containers will be be shut down. They are never shut down until the new containers are
able to respond to requests without errors. This allows us to provide zero-downtime deployments - in the event of a
deployment failure, the old containers will simply continue running without interruption.


Differences between cloud deployment and local builds
-------------------------------------------------------

* **Orchestration**: on the cloud the Control Panel manages orchestration; locally, it's handled by docker-compose
  according to the :ref:`docker-compose.yml <docker-compose-yml-reference>` file.
* **Services**: on the cloud, backing services such as the database and media storage - and if appropriate, optional
  services such as a message queue - are provided from our cloud infrastructure. Locally, these must be handled
  differently (your computer doesn't contain a Postgres cluster or S3 bucket): the database will be provided in a
  separate Docker container, the media storage will be handled via local file storage, and so on. docker-compose will
  configure this local functionality.
* **Docker layer caching** :ref:`on the cloud we don't cache, locally we do <docker-layer-caching>`.
* **Migration commands**: locally these are not executed by default; execute them with :ref:`docker-compose run --rm
  web start migrate <run-migration-commands>`


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
