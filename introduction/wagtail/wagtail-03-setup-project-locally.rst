:sequential_nav: both

..  include:: /introduction/includes/03-local-1-set-up.rst


Start the local project
-------------------------

Start the project by running ``docker-compose up`` in the terminal::

    ➜  docker-compose up
    Starting tutorial-project_db_1
    Performing system checks...

    System check identified no issues (0 silenced).
    May 19, 2020 - 03:29:06
    Django version 2.2.12, using settings 'settings'
    Starting development server at http://0.0.0.0:80/
    Quit the server with CONTROL-C.

Open the project in your web browser by visiting http://127.0.0.1:8000.

(You may notice above that Django claims to be running on port 80, not port 8000. It is - but that's only *inside* the
container. The ``docker-compose.yml`` configuration file is responsible for :ref:`this port-mapping
<docker-compose-web>`.)

..  note::

    If you didn't previously log in to the cloud site before setting up the
    project locally, you'll need to add a user to the database before you can
    log in. The :ref:`Divio SSO system <divio-cloud-sso>` allows you to
    do this from the Django login page with the **Add user** option.

    Or, you could run::

        docker-compose run web manage.py createsuperuser

    See below for more on the use of ``docker-compose``.

``CONTROL-C`` will stop the project.

..  include:: /introduction/includes/03-local-2-useful-commands.rst


..  code-block:: bash

    docker-compose run web python manage.py shell

which will open a Django shell in the ``web`` container.


..  include:: /introduction/includes/03-local-3-next.rst
