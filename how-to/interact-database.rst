.. _interact-database:

How to interact with your project's database
============================================

The Postgres database for your Divio Cloud project runs:

* in a Docker container for your **local** projects: :ref:`interact-local-db`
* on a dedicated cluster for your **Cloud-deployed** sites: :ref:`interact-cloud-db`

In either case, you will mostly only need to interact with the database using the tools provided by
your project's runtime stack (e.g. Django). However, if you need to interact with it directly, the
option exists.


.. _interact-local-db:

Interact with the local database
--------------------------------

This is the recommended and most useful way to interact with the project's database.


From the project's local Django web container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using ``dbshell``
^^^^^^^^^^^^^^^^^

Run::

    docker-compose run --rm web python ./manage.py dbshell


Connecting to a Postgres database manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also make the connection manually from within the ``web`` container, for example::

    docker-compose run --rm web psql -h postgres -U postgres db

As well as ``psql`` you can run commands such as ``pg_dump`` and ``pg_restore``. This is useful
for a number of :ref:`common operations <common-db-operations>`, below.


Using ``docker exec``
.....................

Another way of interacting with the database is via the database container itself, using ``docker
exec``. This requires that the database container already be up and running.

For example, if your database container is called ``example_db_1``::

    docker exec -i example_db_1 psql -U postgres


From your host environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a preferred Postgres management tool that runs on your own computer, you can also
connect to the database from outside the application.


.. _expose-database-ports:

Expose the database's port
^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to the connect to the database from a tool running directly on your
own machine, you will need to expose its port (5432 by default for Postgres).

Add a ports section to the ``db`` service in ``docker-compose.yml`` and map the
port to your host:

..  code-block:: yaml
    :emphasize-lines: 3,4

    db:
        image: postgres:9.4
        ports:
            - 5432:5432

This means that external traffic reaching the container on port 5432 will be
routed to port 5432 internally.

The ports are ``<host port>:<container port>`` - you can choose another host
port if you are already using 5432 on your host.

Now restart the ``db`` container with: ``docker-compose up -d db``


Connect to a Postgres database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need to use the following details:

* port: ``5432``
* username: ``postgres``
* password: not required
* database: ``db``

Access the database using your Postgres tool of choice. Note that you must
specify the host address, ``127.0.0.1``.

For example, if you're using the ``psql`` command line tool, you can connect to the project
database with::

    psql -h 127.0.0.1 -U postgres db


.. _interact-cloud-db:

Interact with the Cloud database
--------------------------------

..  note::

    It's often more appropriate to pull down the Cloud database to a local
    project to interact with it there::

        divio project pull db live  # or test

    See the :ref:`divio project command reference <divio-cli-project-ref>` for more on using these
    commands.


From the project's Cloud application container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  note::

    SSH access to an application container on the Cloud is `available on Managed Cloud projects
    only <http://support.divio.com/control-panel/projects/how-to-ssh-into-your-cloud-server>`_.

Log into your Cloud project's container (Test or Live) over SSH.


Using ``dbshell`` in a Django project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run::

    ./manage.py dbshell

This will drop you into the ``psql`` command-line client, connected to your database.


Connecting to a Postgres database manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also make the connection manually. Run ``env`` to list your environment variables. Amongst
them you'll find ``DATABASE_URL``, which will be in the form::

    DATABASE_URL=postgres://<user name>:<password>@<address>:<port>/<container>

You can use these credentials in the ``psql`` client.


From your own computer
~~~~~~~~~~~~~~~~~~~~~~

Access to Cloud databases other than from the associated application containers is not possible -
it is restricted, for security reasons, to containers running on our own infrastructure.


.. _change-database-version:

Change the local database engine version
----------------------------------------

Sometimes, you will need to change the version of the database engine that your local project uses
- for example if the cloud database is updated or changed. If the two database engines are not the
same, you may run into problems.

The local database engine is specified by the ``image`` option in the ``db`` service in your
project's ``docker-compose.yml`` file, for example:

..  code-block:: yaml
    :emphasize-lines: 2

    db:
        image: postgres:9.6-alpine

Should you need to change this, that line should be updated - for example if the Cloud database is
now running Postgres 11:

..  code-block:: yaml
    :emphasize-lines: 2

    db:
        image: postgres:11-alpine

Docker will use the new version the next time the local project is launched.

If you are not sure what image to use for the local database, Divio support will be able to advise
you.

..  important::

    In the Divio Cloud architecture, the ``docker-compose.yml`` file is **not**
    used for Cloud deployments, but **only** for the local server. The changes you
    make here will not affect the Cloud database.


.. _common-db-operations:

Usage examples for common basic operations
------------------------------------------

It's beyond the scope of this article to give general guidance on using Postgres, but these
examples will help give you an idea of some typical operations that you might undertake while using
Divio Cloud.

All the examples assume that you are interacting with the local database, running in its  ``db``
container.

In each case, we launch the command from within the ``web`` container with ``docker-compose run
--rm web`` and we specify:

* host name: ``-h postgres``
* user name: ``-U postgres``


.. _dump-db:

Dump the database
~~~~~~~~~~~~~~~~~

Dump the database ``db`` to a file named ``database.dump``:

..  code-block:: bash

    docker-compose run --rm web pg_dump -h postgres -U postgres db > database.dump


.. _drop-db:

Drop the database
~~~~~~~~~~~~~~~~~

Drop (delete) the database named ``db``:

..  code-block:: bash

    docker-compose run --rm web dropdb -h postgres -U postgres db


.. _create-db:

Create the database
~~~~~~~~~~~~~~~~~~~~~

Create a database named ``db``:

..  code-block:: bash

    docker-compose run --rm web createdb -h postgres -U postgres db


.. _apply-hstore-db:

Apply the ``hstore`` extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Apply the ``hstore`` extension (required on a newly-created local database) to he database named
``db``:

..  code-block:: bash

    docker-compose run --rm web psql -h postgres -U postgres db -c "CREATE EXTENSION hstore"


.. _restore-db:

Restore the database
~~~~~~~~~~~~~~~~~~~~

Restore a database named ``db`` from a file named ``database.dump``:

..  code-block:: bash

    docker-compose run --rm web pg_restore -h postgres -U postgres -d db database.dump --no-owner


.. _reset-database:

Reset the database
~~~~~~~~~~~~~~~~~~

To reset the database (with empty tables, but the schema in place) you would run the commands above
to :ref:`drop <drop-db>` and :ref:`create <create-db>` the database, :ref:`create the the hstore
extension <apply-hstore-db>`, followed by a migration::

    docker-compose run --rm web python manage.py migrate


Restore from a downloaded Cloud backup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Untar the downloaded ``backup.tar`` file. It contains a ``database.dump`` file. Copy the file to
your local project directory, then run the commands above to :ref:`drop <drop-db>` and :ref:`create
<create-db>` the database, :ref:`create the the hstore extension <apply-hstore-db>`, and then
:ref:`restore from a file <restore-db>`.
