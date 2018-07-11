.. _interact-database:

How to interact with your project's database
============================================

The Postgres database for your Cloud-deployed sites runs on a dedicated
database service.

For local projects, it runs in a Docker container.

Mostly, you will only need to interact with the database via Django. If you need
to interact with it directly, the option exists.

..  warning::

    You use this feature entirely at your own risk. Any error you make could
    cause significant damage to your database. You are strongly advised to
    backup your database before starting.


Cloud database
--------------

From the project's Cloud application container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the feature is `enabled for your project
<http://support.divio.com/control-panel/projects/how-to-ssh-into-your-cloud-serv
er>`_, log into your Cloud project's container (Test or Live) over SSH.

Run ``env`` to list your environment variables. Amongst them you'll find ``DATABASE_URL``, which will be in the form::

    DATABASE_URL=postgres://<user name>:<password>@<address>:<port>/<container>

You can use these credentials in the ``psql`` client, or more conveniently,
run::

    ./manage.py dbshell

which only requires the password.

..  note::

    It's often more appropriate to pull down the Cloud database to a local
    project to interact with it there::

        divio project pull db live  # or test

    See the :ref:`divio project reference <divio-cli-project-ref>` for more.


From your own computer
^^^^^^^^^^^^^^^^^^^^^^

Access to Cloud databases other than from the associated application containers
is not generally possible.


Local database
--------------

To connect to the locally-running database, you will need the following details:

* port: ``5432``
* username: ``postgres``
* password: not required
* database: ``db``

Connecting from the host environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..  important::

    You will need to ensure that your locally-installed Postgres client is
    up-to-date and compatible with the version of Postgres running in our
    database container.

    Once set-up, working from your own local environment using your preferred
    tools will probably suit you best, but some of the configuration will be
    up to you.

    If you have any issues, you can always use our provided method, which is
    guaranteed to work - see :ref:`connecting to the database from within the
    database container <connect-db-within-container>` below.


In order to the connect to the database from a tool running directly on your
own machine, you will need to expose its port (5432).

.. _expose-database-ports:

Expose the database's ports
...........................

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


.. _

Connect to the database
.......................

Access the database using your Postgres tool of choice. Note that you must
specify the host address, ``127.0.0.1``.

If you're using the ``psql`` command line tool, you can connect to the project
database thus::

    psql -h 127.0.0.1 -U postgres db

Or you can issue a general command, for example::

    psql -h 127.0.0.1 -U postgres --list


.. _connect-db-within-container:

From within the database container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each local Divio Cloud project creates a Docker container for its database, and
you can also invoke the ``psql`` tool from directly inside the local database
container.


Identify the container
......................

The database container name ends in ``_db_1`` . If your project is named *My Django
Project*, the container for its database will be ``mydjangoproject_db_1``.

However, you can check using ``docker ps``, which will list the containers.
The right-most column will give you the container names.


Running the command in the container
....................................

To run commands inside the container, use ``docker exec <database container name>``
followed by the command you want to run, for example::

    docker exec mydjangoproject_db_1 psql -U postgres --list

Note that within the container, it's not necessary to specify the host (the
``-h`` option).

Usage examples
^^^^^^^^^^^^^^

It's beyond the scope of this article to give general guidance on using
Postgres, but these examples will help give you an idea of some typical
examples. They indicate what you'd run if you were doing it in each of the two
ways:

* first when running the command from your host computer
* then from within the container with ``docker exec``

Get help
    ``psql -h 127.0.0.1 -U postgres db --help``
    ``docker exec <database container name> psql -U postgres db --help``
Dump the database to a file
    ``pg_dump -h 127.0.0.1 -U postgres db > <file name>``
    ``docker exec pg_dump -U postgres db > <file name>``
Restore from a dumped database file
    ``cat <file name> | psql -h 127.0.0.1 -U postgres db``
    ``cat <file name> | docker exec -i <database container name> psql -U postgres db``


.. _reset-the-database:

Reset the database
..................

One operation you may typically need to perform is to reset the database to its newly-migrated
state, so that it is correctly set up with its schema but no content in its table.

::

    docker ps  # list the containers to find the id you need

    docker exec <database container id> dropdb -U postgres db --if-exists  # drop the database
    docker exec <database container id> createdb -U postgres db  # create the database
    docker exec <database container id> psql -U postgres --dbname=db -c "CREATE EXTENSION IF NOT EXISTS hstore"  # add the hstore extension
    docker-compose run --rm web python manage.py migrate  # migrate the database

This is the state of the database as if the project had been deployed for the first time.
