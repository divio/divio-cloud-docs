..  This include is used by:

    * quickstart-django.rst
    * django-cms-deploy-quickstart.rst



Run the application locally
---------------------------

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

You now have a working, running application ready for further development. All the commands you might normally execute
in development need to be run inside the Docker container -  prefix them with ``docker-compose run web`` as in the
examples above.

You can also use ``docker-compose run web bash`` to get a bash prompt for an interactive session inside the container.


