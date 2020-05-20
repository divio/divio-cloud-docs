.. _how-to-migrate:

How to migrate an existing Django project to Divio
========================================================


Initial project setup
---------------------

Create a new project in the `Divio Control Panel <https://control.divio.com>`_. You'll need to make
sure that the project options are appropriate, including the Python version and project type.

There are a number of available project types, including Django, Django-plus-django CMS and Django-plus-Wagtail, that are already set up with the relevant addon packages.

..  note::

    In general, if the software included in your project already exists on the Divio as an
    Addon, it's recommended to use the packaged addon version. This will help ensure not only that
    it is suitably configured for the Divio Cloud, but that it will also co-exist well with other
    components.

Select the Boilerplate you want to use. Several are available, with different built-in frontend
components to work with. If you choose a complex Boilerplate and later decide that you don't need
its functionality, it's easy to remove from a project. However, select the *Blank Boilerplate* if
you are sure you'd rather to set up and manage your site's frontend starting from scratch.

See :ref:`about-boilerplates` for more on the subject.

Hit **Create project**.

.. important::

    Do not start a deployment yet - we’ll cover that later.


Check addon versions
--------------------

For each of the key components in your project for which a Divio Cloud addon exists, check that it
is set to the correct version in your project, via the project's *Manage addons*. This could
include:

* Django
* django CMS (as well as key applications such as Django Filer, Aldryn News & Blog and so on)
* Wagtail

Note that the version you seek may exist in the *Beta* or *Alpha* release channels of the addon.


Set up the project locally
--------------------------

Once any addons have been appropriately configured, you'll need to set the project up locally. (See
the :ref:`local setup section in the tutorial <replicate-project-locally>` if this is new to you.)

Using the Divio CLI set up a local copy of the project::

    divio project setup <your-project-slug>


Migrate your existing code base
-------------------------------

Add requirements
^^^^^^^^^^^^^^^^

Addons will install their dependencies, so there is no need to add those explicitly as
requirements. Compare the output of::

    docker-compose run --rm web pip list

with your existing project's requirements, or the output of ``pip list`` in its environment, to see
what requirements will need to be added manually. The missing dependencies will need to be added
via the ``requirements.in`` file. See :ref:`install-python-dependencies` for more on adding Python
packages to the project.

Your project may also have some other requirements; see :ref:`install-system-packages`.


Add application code
^^^^^^^^^^^^^^^^^^^^

If your project contains custom applications that are part of the project itself (i.e. they live in
directories inside the project, and are not reusable applications or libraries installed via Pip),
copy them into the project directory.

..  note::

    If you decide in the future that these application should be packaged as reusable addons, that
    can be done later. See :ref:`create-addon`.


Add templates and static files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your project's templates similarly need to be copied to the new project's ``templates`` directory,
and static files to ``static``.


Configure settings
------------------

The settings for your project and its applications need to be added to ``settings.py``.

..  important::

    Do **not** simply copy all your settings into the file. This will not work as expected.

Add them in the appropriate way, which will depend on :ref:`how they are configured <application-configuration>`.


.. _diff_installed_apps:

``INSTALLED_APPS``
^^^^^^^^^^^^^^^^^^

It can be a tedious and error-prone process to get all the ``INSTALLED_APPS`` correct, without
either missing or duplicating any. It will help to get a complete list, sorted alphabetically, and to run a ``diff`` on the list from each project.

Add the following to the end of the ``settings.py`` of both your
source project and the new Divio project::

    for app in sorted(INSTALLED_APPS):
        print(app)

For the original project, run::

    python manage.py shell

and for the Divio project run::

    docker-compose run --rm web python manage.py shell

In each case, copy the list of applications into a file and save the file. Now run a ``diff`` on
the two files::

    diff original-installed-apps new-installed-apps

In the output you will see lines starting with:

* ``>`` - an application present in the Divio project, but not in the original
* ``<`` - an application listed in the original, but not in the Divio project

In the first case, no action is required. In the second case, you may see entries such as::

    < some_application

and you will know that this application has not yet been added to your Divio project's
``INSTALLED_APPS``.

(Once done, don't forget to remove the lines you added.)


Importing content
-----------------

Database
^^^^^^^^

Divio projects use Postgres databases by default, with other options available. It's beyond the scope of this document to
cover all possible eventualities of database importing.


..  note::

    In the examples below ``<container_name>`` will usually be something like
    ``<project_slug>_db_1`` - but you can confirm this by running ``docker ps``::

        ➜  docker ps
        CONTAINER ID  IMAGE         COMMAND                 CREATED            STATUS            PORTS     NAMES
        71fe7e930f60  postgres:9.4  "docker-entrypoint..."  About an hour ago  Up About an hour  5432/tcp  import_project_db_1
        [...]

    The *NAMES* column will list the container name.


Example of Postgres-to-Postgres migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're already using Postgres, you're likely to find that steps along these lines will work:

Drop the database of the newly-created project::

    docker exec <container_name> dropdb -U postgres db --if-exists

Create a new, empty database::

    docker exec <container_name> createdb -U postgres db

Add the ``hstore`` extension::

    docker exec <container_name> psql -U postgres --dbname=db -c "CREATE EXTENSION IF NOT EXISTS
    hstore"

Finally, assuming that you have already dumped your existing database to a local file, import it::

    docker exec -i <container_name> psql -U postgres --dbname db < /path/to/dump


Migrating from one database to another
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to convert your existing database, you can use a conversion script such as https://github.com/lanyrd/mysql-postgresql-converter.

Alternatively, you can export the data to a JSON file (via Django's ``manage.py dumpdata`` command)
and then load it back into the new database with ``manage.py loaddata``.

You may find these resources useful:

* https://github.com/lanyrd/mysql-postgresql-converter
* https://wiki.postgresql.org/wiki/Converting_from_other_Databases_to_PostgreSQL
* https://www.calazan.com/migrating-django-app-from-mysql-to-postgresql/

Once you have loaded your data, check that its migrations are in order, using the ``python
manage.py migrate``.


Media files
^^^^^^^^^^^

Media files should be copied to your project's ``data/media`` directory.


Test the local site
-------------------

You're now in a position to test the local site, which should be done thoroughly. Start it up with::

    divio project up


Upload your changes back to the Divio Cloud
-------------------------------------------

Your project is a Git repository (certain files and directories are excluded), and should be
pushed to the Divio Cloud's Git server in the usual way (``git add``/``git commit``/``git push``).

Media files are not included in the Git repository (static files are however) and must be pushed::

    divio project push media

And the database also needs to be pushed::

    divio project push db

The project can now be deployed on the *Test* server::

    divio project deploy


Upload your project to an independent version control repository
----------------------------------------------------------------

Optionally, you can maintain your project's code in an independent version control repository.

You can `add another Git remote <https://help.github.com/articles/adding-a-remote/>`_ or even a
Mercurial or other remote, and push it there.


