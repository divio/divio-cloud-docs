Check the local site
^^^^^^^^^^^^^^^^^^^^

You may need to perform additional steps such as migrating a database. To run a command manually inside the Dockerised
environment, precede it with ``docker-compose run web``. For example, to run Django migrations: ``docker-compose run
web python manage.py migrate``.

To start up the site locally to test it:

..  code-block:: bash

    docker-compose up

Access the site at http://127.0.0.1:8000/. You can set a different port in the ``ports`` option of
``docker-compose.yml``.
