.. _docker-compose-yml-reference:

The ``docker-compose.yml`` file
===============================

.. _docker-compose-local:

Function of ``docker-compose.yml``
------------------------------------------------------------

..  admonition:: ``docker-compose.yml`` is used exclusively for local project set-up

    In the Divio project architecture, the ``docker-compose.yml`` file is **not** used for cloud deployments, but
    **only** for configuration of the local environment. On the cloud, the deployment is taken care of by dedicated
    systems on our servers.

    This means that entries in or changes to ``docker-compose.yml`` will not affect cloud deployments in any way.

In order to do something useful with containers, they have to be arranged - *orchestrated* - as
part of a project, usually referred to as an 'application'.

There are multiple ways of orchestrating a Docker application, but Docker Compose is probably the most human-friendly. It's what we use for our local development environments.

To configure the orchestration, Docker Compose uses a ``docker-compose.yml`` file. It specifies what images are
required, what ports they need to expose, whether thy e have access to the host filesystem, what commands should be run
when they start up, and so on.


Services defined in ``docker-compose.yml``
------------------------------------------------

In a ``docker-compose.yml`` file, *services* represent the *containers* that will be created in the application.

When you create a new Divio project using one of our *defined project types* (e.g. Aldryn Django or PHP/Laravel using
Flavours) it will include a ``docker-compose.yml`` file ready for local use, with the services already defined.

If you start with a *blank project type*, you will need to assemble the ``docker-compose.yml`` file yourself. This is a
fairly straightforward process once you know what you are doing. Our :ref:`Django tutorial <tutorial-django-set-up>`
includes steps for creating a complete ``docker-compose.yml`` file from scratch. It's a very good way to become familiar
with using Docker Compose, even if you aren't going to be using Django.

For a working local project, various things need to be defined in the file. In a Divio project, there will be a ``web``
service, that's built in a container using the ``Dockerfile``. There will typically also be a ``db`` service, from a
standard ``postgres`` or other database image.

Most Divio projects will use a ``docker-compose.yml`` that contains entries along these lines.

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
     image: postgres:9.6
     volumes:
      - ".:/app:rw"

Some projects will have additional services (such as Celery for example) defined.

Let's look at the components of the file more closely.


.. _docker-compose-web:

The ``web`` service
~~~~~~~~~~~~~~~~~~~


The first definition in the file is for the ``web`` service. In order, the
directives mean:

* ``build``: build it from the ``Dockerfile`` in the current directory
* ``links``: link to the database container (``db``) using the name ``postgres``
* ``ports``: map the *external* port 8000 to the *internal* port 80
* ``volumes``:

  * ``.:/app:rw`` maps the parent directory on the host to ``/app`` in the container, with
    read and write access
  * ``/data:/data:rw`` maps the ``data`` directory on the host to ``/data`` in the container,
    with read and write access

* ``command``: by default, when the command ``docker-compose run`` is issued,
  execute ``python manage.py runserver 0.0.0.0:80`` (this will override the ``CMD`` instruction in the ``Dockerfile``)
* ``env_file``: use the ``.env-local`` to supply environment variables to the
  container

.. _docker-compose-volumes:

The ``volumes`` directive
^^^^^^^^^^^^^^^^^^^^^^^^^

When you execute a ``docker-compose`` command, the ``volumes`` directive in ``docker-compose.yml`` file mounts *source*
directories or volumes from your computer at *target* paths inside the container. If a matching target path exists
already as part of the container image, it will be overwritten by the mounted path.

For example::

    volumes:
      - ".:/app:rw"
      - "./data:/data:rw"

will mount the entire project code (at the relative path ``.``) as the ``/app`` directory inside the container, even
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


.. _docker-compose-env:

Environment variables
^^^^^^^^^^^^^^^^^^^^^

Environment variables are loaded from a file, specified by::

  env_file: .env-local


The ``db`` service
~~~~~~~~~~~~~~~~~~


The second definition is for the ``db`` service. On the cloud, the project's
database runs on an AWS server; locally, it runs on a Postgres instance in
``db``.

The directives mean:

* ``image``: build the container from the ``postgres:9.6`` image
* ``volumes``: map the parent directory on the host to ``/app`` in the
  container, with read and write access

See :ref:`expose-database-ports` for an example of adding configuration to
``docker-compose.yml``.


Further reading
---------------

Our :ref:`Django tutorial <tutorial-django-set-up>` is strongly recommended as a way to learn how a
``docker-compose.yml`` file can be built from scratch to suit your needs.

The :ref:`configure-celery` section describes adding additional services in Docker Compose for a more complex local
set-up.
