.. _docker-compose-yml-reference:

The ``docker-compose.yml`` file
===============================

In order to do something useful with containers, they have to be arranged as
part of a project, usually referred to as an 'application'. This is what a
``docker-compose.yml`` file does, specifying what images are required, what
ports they need to expose, whether the have access to the host filesystem, what
commands should be run, and so on.

.. _docker-compose-local:

..  important::

    In the Divio Cloud architecture, the ``docker-compose.yml`` file is **not**
    used for Cloud deployments, but **only** for the local server. On the Cloud,
    the deployment is taken care of by dedicated systems on our servers.

The ``docker-compose.yml`` in Divio Cloud projects builds a ``web`` service in
a container using its ``Dockerfile``. It also builds a ``db`` service, from a
standard ``postgres:9.4`` image.

Most Divio Cloud projects will use this ``docker-compose.yml``, or something
very similar to it.

..  code-block:: yaml

    web:
     build: .
     links:
      - "db:postgres"
     ports:
      - "8000:80"
     volumes:
      - ".:/app:rw"
      - "./data:/data:rw"
     command: python manage.py runserver 0.0.0.0:80
     env_file: .env-local
    db:
     image: postgres:9.4
     volumes:
      - ".:/app:rw"

The ``web`` service
-------------------


The first definition in the file is for the ``web`` service. In order, the
directives mean:

* ``build``: build it from the ``Dockerfile`` in the parent directory
* ``links``: link to the database container
* ``ports``: map the external port 8000 to the internal port 80
* ``volumes``:
    * map the parent directory on the host to ``/app`` in the container, with
      read and write access
    * map the ``data`` directory on the host to ``/data`` in the container,
      with read and write access
* ``command``: by default, when the command ``docker-compose run`` is issued,
  execute ``python manage.py runserver 0.0.0.0:80``
* ``env_file``: use the ``.env-local`` to supply environment variables to the
  container

.. _docker-compose-volumes:

The ``volumes`` directive
~~~~~~~~~~~~~~~~~~~~~~~~~

When you execute a ``docker-compose`` command, the ``volumes`` directive in ``docker-compose.yml`` file mounts *source*
directories or volumes from your computer at *target* paths inside the container. If a matching target path exists
already as part of the container image, it will be overwritten by the mounted path.

For example::

    volumes:
      - ".:/app:rw"
      - "./data:/data:rw"

will mount the entire project code (at the relative path ``.``) as the ``/app`` directory inside the container, *even
if there was already an ``/app`` directory there*, in *read-write* mode (i.e. the container can write as well as
read files on the host).

This allows you to make changes to the project from your computer during the local development process, that will be
picked up by project inside Docker. These changes will be available to the project only as long as the host directory
is mounted inside the container. In order to be made permanent, they need to be committed into the repository so that
they will be picked up when the image and container are rebuilt.

..  admonition:: Implications for local testing

    Nearly everything in ``/app`` in the container is also present in the project repository and thus on the host
    machine. This means that it is safe to replace the container's ``/app`` files with those from the host.

    However, any files in ``/app`` that are placed there during the build process, i.e. the execution of the
    ``Dockerfile``, **will not be available in the local environment**. For a standard Django project, these will
    include:

    * the compiled pip requirements, in ``requirements.txt``
    * collected static files, in ``static_collected``

    In most cases, this will not matter, but sometimes these files are required in local development. For example, the
    ``requirements.txt`` may contain useful information about dependency relationships, or the ``Dockerfile`` may have
    performed custom processing of static files.

    In that case, the ``- ".:/app:rw"`` line can be commented out in ``docker-compose.yml``. In this case, the
    container will use the files baked into the image, and will not use the local host's files.

    This will allow local configuration to replicate the cloud environment even more closely.


The ``db`` service
------------------


The second definition is for the ``db`` service. On the Cloud, the project's
database runs on an AWS server; locally, it runs on a Postgres instance in
``db``.

The directives mean:

* ``image``: build the container from the ``postgres:9.4`` image
* ``volumes``: map the parent directory on the host to ``/app`` in the
  container, with read and write access

See :ref:`expose-database-ports` for an example of adding configuration to
``docker-compose.yml``.
