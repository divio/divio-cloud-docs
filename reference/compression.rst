.. _compression:

File compression in Divio Django applications
===============================================

Default behaviour in our projects
---------------------------------

By default, we apply gzip compression to:

* Django-served content, such as HTML files
* static files, when ``DEBUG`` is ``False``

This compression can be disabled by setting the ``DISABLE_GZIP`` environment variable to ``True``.

For Django-served content, we apply Django’s :mod:`GZipMiddleware <django.middleware.gzip>`.

For static files, we use our own :setting:`STATICFILES_STORAGE` classes to gzip static files after they are collected.
See ``GZippedStaticFilesMixin.post_process()``, in `Aldryn Django's storage.py
<https://github.com/divio/aldryn-django/blob/support/2.1.x/aldryn_django/storage.py>`_.


Using ``DISABLE_GZIP``
~~~~~~~~~~~~~~~~~~~~~~

When gzip is disabled, gzipped versions of static files are not used (though they are still collected). A default
Django storage class is used instead.


Using ``DEBUG = True``
~~~~~~~~~~~~~~~~~~~~~~

When ``DEBUG = True``, the non-gzipped versions of the files are loaded by templates, whether or not
``DISABLE_GZIP`` has been applied.


Using Django Compressor
-----------------------

`Django Compressor <https://django-compressor.readthedocs.io/en/stable/>`_ is a popular tool for additional compression
functionality (for example, consolidation of multiple files into one).

When using Django Compressor, note that:

* `offline compression must be used <https://django-compressor.readthedocs.io/en/stable/usage#offline-compression>`_
* static files must be compressed *before* collection (``python manage.py compress`` must come before ``collectstatic``
  in the ``Dockerfile``)

To verify correct and expected operation of Django Compressor, :ref:`use the local server in live configuration
<local-in-live-mode>`, taking note to :ref:`disable volume mapping that would affect the collected compressed files <local-live-volumes>`.
