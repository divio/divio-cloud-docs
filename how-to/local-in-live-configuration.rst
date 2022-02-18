.. _local-in-live-mode:

How to run a local application in live configuration
====================================================

The local and cloud Docker application environments are as close as possible, to help guarantee
that your applications will run in just the same way across all of them.

However, there are a few differences. See :ref:`default-project-conditions` for the default
configuration in each environment.

Occasionally, you may wish to run the local server in a configuration closer to the live set-up. A few steps are needed
to achieve this. You may not need to take all of these steps - it depends which aspects of the environment matter in
your particular case.


..  _local-live-volumes:

Isolate the container's file system from your own
--------------------------------------------------------------------------------------

For development purposes, it's often useful to map the host filesystem to the working directory - usually ``/app`` -
inside the container. The :ref:`volumes configuration in the docker-compose.yml file <docker-compose-volumes>`
therefore overwrites directories inside the container with directories from your own file system:

..  code-block:: yaml

    volumes:
      - ".:/app:rw"         # overwrites /app with the entire project directory

This is useful because it allows you to make changes on your filesystem such as code changes and have them immediately
reflected inside the container.

However, it does overwrite any files that belong to the image, inside the container, each time a container is launched
using ``docker-compose``.

This does not occur in cloud deployments. To ensure that your application sees the same files locally that it does in
the cloud, comment out the mapping.


Ensure the application runs in a production configuration
---------------------------------------------------------

Your application may run in a different configuration in different environments. Apply any relevant environment
variables locally that your application would use in production. These could include:

* ``STAGE``
* ``DEBUG``

and so on.


.. _run-migration-commands:

Run the release commands
---------------------------

:ref:`Release commands <release-commands>` are run during deployment after the image build has completed
successfully. They are not run automatically locally. Execute them with:

..  code-block:: bash

    docker-compose run web <command>

Legacy Aldryn Django applications can have their release commands executed with:

..  code-block:: bash

    docker-compose run web start migrate

(In an Aldryn Django project, you can see these commands listed in the ``MIGRATION_COMMANDS`` setting, populated by
applications using the addons framework).


.. _use-cloud-storage:

Use the cloud media storage rather than local file storage
----------------------------------------------------------

Your local project will use local file storage rather than the cloud storage. Usually this is most
appropriate for development, and also faster and more convenient than using the remote cloud storage. However,
sometimes you might want to use the cloud storage when the application is running locally.

Cloud storage configuration values are provided in the ``DEFAULT_STORAGE_DSN`` environment variable.

In order to use the cloud storage locally, find the value of ``DEFAULT_STORAGE_DSN`` using the :ref:`divio app
env-vars <reading-env-vars>` command, and add the variable to the ``.env-local`` file (this works for applications that
are able to parse the value).


.. _use-cloud-database:

Using the cloud database rather than a local instance
----------------------------------------------------------

Your project uses our database cluster on the cloud. Locally, it sets up the same database in its own container.

The databases for our public regions are not accessible except from containers running on our own infrastructure, for
security reasons. Access can be made possible for databases on private clusters only.


Use the production web server
-----------------------------

The :ref:`docker-compose.yml file <docker-compose-yml-reference>` launches your website for local use only, overriding
the ``CMD`` in the ``Dockerfile`` that's used in the cloud.

To start up the application using the ``CMD`` specified by the ``Dockerfile`` instead, comment out the
``docker-compose.yml``'s ``command``.

(In legacy Aldryn Django applications, change the ``command`` to ``start web``.)


Other configuration
--------------------

Note that some aspects of the cloud configuration are harder to replicate locally, such as your container's RAM
allocation or its interaction with our ingress controller and other infrastructure. A cloud application may use
services that are not accessible locally. We recommend using a cloud environment as part of the testing and quality
assurance process.
