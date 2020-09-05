:sequential_nav: both

.. _tutorial-django-static:

Configure static file serving
===================================

The site's static files need to be handled properly.

As mentioned previously, when using the runserver locally you are able to load the Django admin's CSS at
http://127.0.0.1:8000/static/admin/css/fonts.css; this is because the Django runserver takes care of serving static
files for you. When running with Uvicorn instead of the runserver, the file is not served. If you try to load the same
file from the cloud server, where the ``Dockerfile`` launches the site with Uvicorn, you'll have a similar experience.

When running with a production server like Uvicorn, you need to configure static file serving explicitly. There are
multiple ways to do this, but one very good way to do so on the Divio infrastructure is to use the Python library
`WhiteNoise <http://whitenoise.evans.io>`_. WhiteNoise is designed to work behind Content Delivery Networks and
integrates well with Django.

Add ``whitenoise`` to the ``requirements.txt``:

..  code-block:: text

    whitenoise==5.2.0

In ``settings.py``, add it to the list of ``MIDDLEWARE``, after the ``SecurityMiddleware``:

..  code-block:: python
    :emphasize-lines: 3

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        [...]
    ]

And to have it cache and compress static files, and to tell Django where to put collected static files, add:

..  code-block:: python
    :emphasize-lines: 2-3

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

Rebuild the image to have WhiteNoise installed.

You can check that Uvicorn and WhiteNoise are serving the static files as expected by:

* commenting out the ``command`` line in ``docker-compose.yml`` (to ensure that the runserver isn't handling them), and
* setting ``DEBUG`` in ``settings.py`` to ``False`` (to ensure that they aren't being served by :ref:`Django's built-in
  static file serving <django:serving-static-files-in-development>`).

Collect the static files to their destination for serving:

..  code-block:: bash

    docker-compose run web python manage.py collectstatic

And now you should be able to load http://127.0.0.1:8000/static/admin/css/fonts.css.

Commit and push your changes (first revert the temporary changes to ``docker-compose.yml`` and ``settings.py``).
Deploy the Test environment, and check that static files work as expected there too.

------------

The project can now handle static files, and will do so in an appropriate way for whichever environment the code is
running in. The next step is to configure storage and serving of media (i.e. user-uploaded) files.
