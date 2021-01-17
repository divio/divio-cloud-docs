..  Do not change this document name!
    Referred to by: https://github.com/divio/django-divio-quickstart
    Where: in the README
    As: https://docs.divio.com/en/latest/how-to/django-deploy-quickstart/

.. meta::
   :description:
       The quickest way to get started with Django on Divio. This guide shows you how to use the Django Divio
       quickstart repository to deploy a Twelve-factor Django project including Postgres or MySQL, and cloud media
       storage using S3, with Docker.
   :keywords: Docker, Django, Postgres, MySQL, S3


Deploy a new Django project using the Divio quickstart repository
====================================================================

The `Django Divio quickstart <https://github.com/divio/django-divio-quickstart>`_ repository is a template that gives
you the fastest possible way of launching a new Django project on Divio.

It uses a completely standard Django project as created by the Django ``startproject`` management command.

The only additions are a few lines of glue code in ``settings.py`` to handle configuration using environment variables,
plus some additional files to take care of the Docker set-up.


Clone the repository
--------------------

Run:

..  code-block:: bash

    git clone git@github.com:divio/django-divio-quickstart.git

The project contains a module named ``quickstart``, containing ``settings.py`` and other project-level configuration.


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

then:

..  code-block:: bash

    docker-compose run web python manage.py createsuperuser


Launch the local server
~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: bash

    docker-compose up

You can log in to the site at http://127.0.0.1:8000/admin.

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
