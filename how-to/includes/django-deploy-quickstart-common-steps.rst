..  This include is used by:

    * django-deploy-quickstart.rst
    * django-cms-deploy-quickstart.rst

Renaming the ``quickstart`` project module (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you'd like this to be named something else, now is the time to change the directory name, along with the references
to the ``quickstart`` module wherever it appears, which is in:

* ``Dockerfile``
* ``manage.py``
* ``asgi.py``
* ``settings.py``
* ``wsgi.py``


Using MySQL or an alternative gateway server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the project uses Postgres and uWSGI, but MySQL and other gateway server options are available.

You'll need to change a few lines of configuration to achieve this across a few files. See the notes for each:

* :ref:`requirements.txt <django-create-deploy-requirements>`
* :ref:`docker-compose.yml <django-create-deploy-docker-compose>`
* :ref:`env-local <django-create-deploy-env-local>`
* :ref:`the Dockerfile <django-create-deploy-CMD>`


Run the project locally
-----------------------

This section assumes that you have Docker and the Divio CLI installed. You also need an account on Divio, and your
account needs your SSH public key. See :ref:`local-cli` if required.


Build the Docker image
~~~~~~~~~~~~~~~~~~~~~~

Run:

..  code-block:: bash

    docker-compose build


Run database migrations and create a superuser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: bash

    docker-compose run web python manage.py migrate

(Note that due to Docker behaviour, you may get an error the first time you run this - Docker can sometimes be too
slow to start up the database in time. If this happens, simply run the command again.)

then:

..  code-block:: bash

    docker-compose run web python manage.py createsuperuser


Launch the local server
~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: bash

    docker-compose up

You can log in to the site at:

* http://127.0.0.1:8000/ (this will work if a URL has been wired up to `/`)
* http://127.0.0.1:8000/admin

You now have a working, running project ready for further development. All the commands you might normally execute
in development need to be run inside the Docker container, but preceding them with ``docker-compose run web`` as in the
examples above.

You can also use ``docker-compose run web bash`` to get a bash prompt for an interactive session inside the container.


Deploy the project to Divio
------------------------------

The project is ready for cloud deployment. This requires creating a project on the Divio platform.


Create a new project on Divio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the `Divio Control Panel <https://control.divio.com>`_ add a new project, selecting the *Build your own* option.


Add database and media services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new project does not include any additional services; they must be added manually. Use the *Services* menu to add a
Postgres or MySQL database as appropriate, and an S3 object storage instance for media.


Connect the local project to the cloud project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your Divio project has a *slug*, based on the name you gave it when you created it. Run ``divio project list -g`` to
get your project's slug; you can also read the slug from the Control Panel.

Run:

..  code-block:: bash

    divio project configure

and provide the slug. This creates a new file in the project at ``.divio/config.json``. ``divio project dashboard``
will open the project in the Control Panel.

The command also returns the Git remote value for the project. You'll use this in the next step.


Configure the Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the project's Git repository as a remote, using the value obtained from the ``divio project configure`` command above, for example:

..  code-block:: bash

    git remote add divio git@git.divio.com:django-project.git


Commit (if required) and push
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you made any changes to the project files, you will need to commit them first. Otherwise you can simply push to
the new remote:

..  code-block:: bash

    git push divio main


..  important::

    Check the Git branch for the Test environment in the *Environments* view of your project, and if necesssary,
    change it to ``main`` to match the local repository.


..  include:: /how-to/includes/django-deploy-test-working-database.rst


Additional notes
-----------------

See :ref:`working-with-recommended-django-configuration` for further guidance.