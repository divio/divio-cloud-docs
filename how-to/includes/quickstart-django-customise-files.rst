..  This include is used by:

    * quickstart-django-common-steps.rst
    * django-cms-deploy-quickstart.rst

Renaming the ``quickstart`` application module (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you'd like this to be named something else, now is the time to change the directory name, along with the references
to the ``quickstart`` module wherever it appears, which is in:

* ``Dockerfile``
* ``manage.py``
* ``asgi.py``
* ``settings.py``
* ``wsgi.py``


Using MySQL or an alternative gateway server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the application uses Postgres and uWSGI, but MySQL and other gateway server options are available.

You'll need to change a few lines of configuration to achieve this across a few files. See the notes for each:

* :ref:`requirements.txt <deploy-django-requirements>`
* :ref:`docker-compose.yml <deploy-django-docker-compose>`
* :ref:`env-local <deploy-django-env-local>`
* :ref:`the Dockerfile <deploy-django-CMD>`
