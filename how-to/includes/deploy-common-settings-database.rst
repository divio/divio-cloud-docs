Database
~~~~~~~~~~~

Database credentials, if required, are provided in a ``DATABASE_URL`` environment variable. When a database (and
therefore the environment variable) are not available (for example during the Docker build phase) the application
should fall back safely, to a null database option or to an in-memory database (e.g. using ``sqlite://:memory:``).

See the Django guide for :ref:`a concrete example <deploy-django-database>`.

