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


The second definition is for the ``db`` service. On the Cloud, the project's
database runs on an AWS server; locally, it runs on a Postgres instance in
``db``.

The directives mean:

* ``image``: build the container from the ``postgres:9.4`` image
* ``volumes``: map the parent directory on the host to ``/app`` in the
  container, with read and write access

See :ref:`expose-database-ports` for an example of adding configuration to
``docker-compose.yml``.
