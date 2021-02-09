..  This include is used by:

    * django-deploy-quickstart.rst
    * django-cms-deploy-quickstart.rst



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

Try accessing the site at http://127.0.0.1:8000/ (this will only work if a URL has been wired up to `/`).

The Django admin is available at http://127.0.0.1:8000/admin.

You now have a working, running project ready for further development. All the commands you might normally execute
in development need to be run inside the Docker container -  prefix them with ``docker-compose run web`` as in the
examples above.

You can also use ``docker-compose run web bash`` to get a bash prompt for an interactive session inside the container.


Deploy the project to Divio
------------------------------

The project is ready for cloud deployment. This requires creating a project on the Divio platform.


Create a new project on Divio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the `Divio Control Panel <https://control.divio.com>`_ add a new project, selecting the *Build your own* option.
Accept all the defaults including the Git repository options.


Add database and media services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The new project does not include any additional services; they must be added manually. Use the *Services* menu to add a
Postgres or MySQL database as appropriate, and an S3 object storage instance for media.


..  include:: /how-to/includes/connect-local-to-cloud.rst


Configure the Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the project's Git repository as a remote, using the value obtained from the ``divio project configure`` command above. For example:

..  code-block:: bash

    git remote add divio git@git.divio.com:my-divio-project.git


Commit (if required) and push
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you made any changes to the project files, you will need to commit them first. Otherwise you can simply push to
the new remote:

..  code-block:: bash

    git push divio main


..  important::

    Check the Git branch for the Test environment in the *Environments* view of your project, and if necessary,
    change it to ``main`` to match the local repository.


..  include:: /how-to/includes/django-deploy-test-working-database.rst


Additional notes
-----------------

See :ref:`working-with-recommended-django-configuration` for further guidance.
