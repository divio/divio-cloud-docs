:sequential_nav: both

.. _tutorial-django-database:

Add and configure a Postgres database
=====================================

In this section, we'll configure the application to use a Postgres database, both locally for development, and on the
cloud for deployment.

..  important::

    For this part of the tutorial you will need to be opted-in to Beta features on the Divio Control Panel. You can do
    this in your `account settings <https://control.divio.com/account/contact/>`_.


Create the database
--------------------------------

For the cloud environments
~~~~~~~~~~~~~~~~~~~~~~~~~~

In the project's :ref:`Services <services>` view, add a PostgreSQL database. When you next deploy, or if you manually
select *Provision* from the services options menu, it will be provisioned for the project (you need to do one of those
now).

.. image:: /images/intro-services.png
   :alt: 'The Services view'
   :class: 'main-visual'


Locally
~~~~~~~

For development purposes when working locally, we should also have a database. It's not so easy to set up the right
version of Postgres locally, especially when working with different projects, and as a result many Django developers
content themselves with using SQLite locally, because it's an easy-to-use default. However, it's much better to use the
same database in development as you do in deployment, and Docker Compose can take care of this for you too. Edit your
``docker-compose.yml`` to add some new lines:

..  code-block:: YAML
    :emphasize-lines: 16-

    version: "2"

    services:

      web:
        # the application's web service (container) will use an image based on our Dockerfile
        build: "."
        # Map the internal port 80 to port 8000 on the host
        ports:
          - "8000:80"
        # Map the host directory to app (which allows us to see and edit files inside the container)
        volumes:
          - ".:/app:rw"
        # The default command to run when launching the container
        command: python manage.py runserver 0.0.0.0:80
        # the URL 'postgres' will point to the application's db service
        links:
          - "db:postgres"

      db:
        # the application's web service will use an off-the-shelf image
        image: postgres:9.6-alpine
        environment:
          POSTGRES_DB: "db"
          POSTGRES_HOST_AUTH_METHOD: "trust"
        volumes:
          - ".:/app:rw"

The next time you launch the application locally, it will include a Postgres database running in a ``db`` container.


Configure database access using an environment variable
-------------------------------------------------------

Configuration for application services is `stored in environment variables, following the Twelve-Factor model
<https://www.12factor.net/config>`_. These variables will need to be parsed by the application. For the database the
values are provided via an environment variable named :ref:`DEFAULT_DATABASE_DSN <env-var-database-dsn>`, a *Data
Source Name*, in the general form::

    scheme://username:password@host:port/path?query#fragment

The variables are provided in the cloud environments as soon as the service is provisioned. We should add a variable
to the local environment too. The easiest way to do this is again with the help of ``docker-compose.yml``.

First, create a new file called ``.env-local``, and add the variable to it:

..  code-block:: text

    DEFAULT_DATABASE_DSN=postgres://postgres@postgres:5432/db

If you're familiar with Postgres, you'll recognise its default user and port in the URL.

Then add a new line to the ``web`` section in ``docker-compose.yml`` to tell it where it should find the variables for
the environment it creates:

..  code-block:: YAML
    :emphasize-lines: 5

      web:
        [...]
        links:
          - "db:postgres"
        env_file: .env-local

Now in every runtime environment, the application will find the correct database connection values; in a cloud
environment, it will find variables provided by the cloud infrastructure, while locally it will use the ones we supply
via ``.env-local``.

Again, this follows the Twelve-Factor principles. `We manage one codebase in version control, and deploy exactly the
same codebase in every deployment <https://www.12factor.net/codebase>`_ - even locally.


Use the environment variable in our settings
--------------------------------------------

The next task is to connect the application to the database (we will use the Python ``psycopg2`` library) and parse the
URL with connection details (using ``dj_database_url``).

List both libraries in ``requirements.txt``:

..  code-block:: YAML
    :emphasize-lines: 3-

    django==3.1
    uvicorn==0.11.8
    psycopg2==2.8.5
    dj_database_url==0.5.0

Rebuild the image once more to include the new packages.

Then in ``settings.py``, add (replacing the existing ``DATABASES`` setting):

..  code-block:: python

    import os
    import dj_database_url

    [...]

    DEFAULT_DATABASE_DSN = os.environ.get('DEFAULT_DATABASE_DSN')
    DATABASES = {'default': dj_database_url.parse(DEFAULT_DATABASE_DSN)}

We're now in a position to use the database for the first time. The first thing to do is create Django's tables, by
running migrations, and then add an admin user to the database:

..  code-block:: bash

    docker-compose run web python manage.py migrate
    docker-compose run web python manage.py createsuperuser

The next time you run ``docker-compose up``, you'll be able to `log in to the admin <http://127.0.0.1:8000/admin>`_.
(If you don't see the expected styling of the Django admin, it's probably because the site is running with Uvicorn
rather than the runserver - check whether you left the ``command`` line in ``docker-compose.yml`` commented out.)


Deploy your changes
-------------------

It is worth verifying that the site now runs on the cloud too. Commit the changes you've made:

..  code-block:: bash

    git add docker-compose.yml myapp requirements.txt .env-local
    git commit -m "Added database configuration"
    git push

and deploy:

..  code-block:: bash

    divio project deploy

..  sidebar:: Pushing ``.env-local``
    :subtitle: Configuration secrets should not be committed to code repositories.

    In this case, there is nothing in ``.env-local`` that can't be safely committed, and having the
    ``DEFAULT_DATABASE_DSN`` in there means that if a colleague needs to set up your Divio project, they will that in
    there too, ready to use in their own local environment. However if you were testing functionality that required you
    add a secret key, for example to use some external service, you should take care not to commit that.

Your local database has been migrated and you have created an admin superuser. In the cloud environment, the Django
database tables have not yet been created, so if you try to access the admin there, you'll naturally get an error:

..  code-block:: text

    ProgrammingError at /admin/login/
    relation "auth_user" does not exist
    LINE 1: ...user"."is_active", "auth_user"."date_joined" FROM "auth_user...

The Divio CLI includes a very convenient way to upload your local database to the cloud. Run:

..  code-block:: bash

    divio project push db

This will push the local database to the cloud Test environment. Once the process has completed, you can refresh the
cloud Test site; you'll be able to log in at ``/admin`` with your admin user credentials.

Similarly, you can push/pull media files, and also specify which cloud environment to target. See the :ref:`local
commands cheatsheet <cheatsheet-project-resource-management>`. A common use-case is to pull live content into the
development environment, so that you can test new development with real data.

You can also execute commands like ``python manage.py migrate`` directly in the cloud environment. Copy the SSH URL
from the Test environment pane in the Control Panel, and use it to open a session directly to a cloud container. Then
run:

..  code-block:: bash

    python manage.py migrate

-------------------

You now have a production-ready database, for your cloud environments, and the same database engine running locally,
with a convenient way to move content between them. Your codebase remains clean - it's the same codebase in all those
environments - and configuration is devolved to its environments.

In the next section, we'll configure static file serving.

