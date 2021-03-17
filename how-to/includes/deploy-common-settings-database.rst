Database
~~~~~~~~~~~

Database credentials are provided in a ``DATABASE_URL`` environment variable. When a database (and therefore the
environment variable) are not available (for example during the Docker build phase) the application should fall back
safely, to a null database option or to an in-memory database (e.g. using ``sqlite://:memory:``).

For Django, we recommend:

..  code-block:: python

    # Configure database using DATABASE_URL; fall back to sqlite in memory when no
    # environment variable is available, e.g. during Docker build
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite://:memory:')

    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
