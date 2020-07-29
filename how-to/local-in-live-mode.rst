.. _local-in-live-mode:

How to run a local project in live configuration
================================================

The Local, Test and Live server environments are as identical as possible, to help guarantee
that your applications will run in just the same way across all of them.

However, there are a few differences. See :ref:`default-project-conditions` for the default
configuration in each environment.

Occasionally, you may wish to run the local server in a configuration closer to the live set-up. A few steps are needed
to achieve this. You may not need to take all of these steps - it depends which aspects of the environment matter in
your particular case.


Build the project
-----------------

Build the project in the normal way (``docker-compose build web``) if there have been any changes to it.


..  _local-live-volumes:

Isolate the container's file system from your own
--------------------------------------------------------------------------------------

The :ref:`default volumes configuration in the docker-compose.yml file
<docker-compose-volumes>` overwrites directories inside the container with directories from your own file system:

..  code-block:: yaml

    volumes:
      - ".:/app:rw"         # overwrites /app with the entire project directory
      - "./data:/data:rw"   # overwrites /data with the entire data directory

This is useful for development purposes, because it allows you to make changes on your filesystem such as code changes
and have them immediately reflected inside the container. Additionally, it allows media files (which are not included
in the image) that you pull to your local environment to be made available inside the container at ``/data``.

However, it does overwrite any files in either of these locations that belong to the image, inside the container, each
time a container is launched using ``docker-compose``.

This does not occur in cloud deployments, so you will often want to prevent this when running a local project in
live configuration.

For example, our Aldryn Django ``Dockerfile`` contains a ``collectstatic`` command that collects static files at
``/static_collected`` in the image. Most of the time, it doesn't matter that these are overwritten in the local
environment container, because by default it runs Django in ``DEBUG`` mode and serves the files from the installed
packages. To run in the same conditions as on the cloud, these files need to be served from the ``/static_collected``
directory that was created by the image, so that needs to be available.

Comment out the line:

..  code-block:: yaml

    - ".:/app:rw"

in order to protect the image's files from being overwritten in the container.

(Note that once you do this, you can no longer amend files inside the container by making changes on your files system.)


Ensure the application runs in a production configuration
---------------------------------------------------------

Your application may run in a different configuration in different environments.

The ``STAGE`` :ref:`environment variable <environment-variables>` in the file ``.env-local`` provides the
application with information about the environment. Use:

..  code-block:: text

    STAGE=live

There may be specific environment variables that also need to be checked. For example, Aldryn Django projects
run in  ``DEBUG`` mode locally, in which case you'd also need:

..  code-block:: text

    DEBUG=False


.. _run-migration-commands:

Run the ``migrate`` command
---------------------------

Migration commands, also known as release commands, are run during deployment *after* the image build has completed
successfully. They are not run automatically locally, but you can execute them with:

..  code-block:: bash

    docker-compose run --rm web start migrate

(In an Aldryn Django project, you can see these commands listed in the ``MIGRATION_COMMANDS`` setting, populated by
applications using the addons framework).


.. _use-cloud-storage:

Use the cloud media storage rather than local file storage
----------------------------------------------------------

Your local project will use local file storage rather than the cloud storage. Cloud media files are pulled to the local
environment when you run ``divio project setup`` (or later, ``divio project pull media``). Usually this is most
appropriate for development, and also faster and more convenient than using the remote cloud storage. However,
sometimes you might want to use the cloud storage when the application is running locally.

Aldryn Django will use the ``DEFAULT_STORAGE_DSN`` environment variable to configure storage. This is provided in all
cloud environments (each environment gets its own value). If the variable is not present, Aldryn Django will revert to
using :mod:`FileSystemStorage <django:django.core.files.storage>` (Django's default), which is what happens locally.

In order to use the cloud storage instead, find the value of ``DEFAULT_STORAGE_DSN`` using the :ref:`divio project
env-vars <reading-env-vars>` command, and add the variable to the ``.env-local`` file. The next time you start the
container, it will use the cloud storage.


.. _use-cloud-database:

Use the cloud database rather than a local instance
----------------------------------------------------------

Your project uses our database cluster on the cloud. Locally, it sets up the same database in its own container.

The databases for our public regions are not accessible except from containers running on our own infrastructure, for
security reasons. Access can be made possible for databases on private clusters only.


Use the production web server
-----------------------------

The :ref:`docker-compose.yml file <docker-compose-yml-reference>` launches your website, but doesn't necessarily do it
the way it would be launched on the cloud. For example, in Aldryn Django projects, it uses the Django ``runserver``
command, whereas the cloud environments use uWSGI.

To the production web server (using uWSGI, and serving static files) rather than the Django
runserver, change:

..  code-block:: yaml

    command: python manage.py runserver 0.0.0.0:80

to:

..  code-block:: yaml

    command: start web

With other project types, you will need to amend the command suitably.

The local server will now be running in a configuration much closer to that of the live project.