.. _aldryn-django:

Aldryn Django (core Django)
===========================

Aldryn Django (``aldryn-django``) is a wrapper application that installs and provides basic
configuration for Django.

See `aldryn-django.aldryn_config <https://github.com/aldryn/aldryn-django/tree/support/2.1.x>`_
(ensure that you switch to the correct branch) for the all settings it takes and how they are
applied.

Most of the key settings are listed below.


Control Panel options
---------------------

Some settings are exposed in the Aldryn Addon configuration form in the Control Panel. These
settings will take priority over those entered as environment variables or in ``settings.py``.


.. _hash-static-file-names:

*Hash static file names*
~~~~~~~~~~~~~~~~~~~~~~~~

The Aldryn Django addon includes a *Hash static file names* option. When selected, Django's
:class:`ManifestStaticFilesStorage
<django:django.contrib.staticfiles.storage.ManifestStaticFilesStorage>` will be used as the storage
backend. This appends an MD5 hash of each file's contents to its filename, allowing caching headers
to be safely set in the far future.

Aldryn Django configures uWSGI to set the ``Cache-Control`` header to one year on files with a
hash in the filename.


*Enable django.contrib.gis*
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enables GeoDjango support. Adds ``django.contrib.gis`` to ``INSTALLED_APPS`` and sets the database
engine to ``django.contrib.gis.db.backends.postgis``.

For local development you will need to edit ``docker-compose.yml``, changing ``postgres:9.6`` to
``mdillon/postgis:9.6``. On the Cloud, you will need to make a support request to have the new
database enabled for the project.


.. _PREFIX_DEFAULT_LANGUAGE:

*Remove URL language prefix for default language*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When set, will add ``aldryn_django.middleware.LanguagePrefixFallbackMiddleware`` to the middleware.

This will cause Django **not** to use a language prefix in the URL when serving the default
language. For example, by default, ``/about`` will redirect to ``/en/about`` if English is the
default language; with this option selected, it will not (and will instead redirect in the other
direction).

Note that prior to Django version 1.10, this will not work with projects in which
multiple languages are defined.

This is a ``302 Temporary Redirect``, as determined in Django's core. It is not
safe to use permanent redirects here, because language redirects are
content-dependent. A change in the site could cause redirect loops, as
described at :ref:`301vs302`, or spurious 404 errors.


*Timeout for users session, in seconds*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See ``SESSION_COOKIE_AGE`` in :ref:`session-middleware-settings`.


Environment variable/``settings.py`` options
--------------------------------------------

Security-related settings
~~~~~~~~~~~~~~~~~~~~~~~~~

.. _security-middleware-settings:

Security middleware settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each of these settings can be specified as an environment variable (recommended except where
indicated otherwise below) or in ``settings.py``. These settings apply to Django's :mod:`Security
middleware <django:django.middleware.security>`.

* :setting:`django:SECURE_BROWSER_XSS_FILTER` (default: ``False``)
* :setting:`django:SECURE_CONTENT_TYPE_NOSNIFF` (default: ``False``)
* :setting:`django:SECURE_HSTS_INCLUDE_SUBDOMAINS` (use ``settings.py``; not available as an
  environment variable)
* :setting:`django:SECURE_HSTS_PRELOAD` (use ``settings.py``; not available as an environment
  variable)
* :setting:`django:SECURE_HSTS_SECONDS` (default: 0)
* :setting:`django:SECURE_REDIRECT_EXEMPT` (use ``settings.py``; not available as an environment
  variable)
* :setting:`django:SECURE_SSL_HOST` (use ``settings.py``; not available as an environment variable)
* :setting:`django:SECURE_SSL_REDIRECT` (default: ``None``)


.. _session-middleware-settings:

Session middleware settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :setting:`django:SESSION_COOKIE_HTTPONLY` (must be ``False`` for django CMS, default: ``False``)
* :setting:`django:SESSION_COOKIE_SECURE` (default: ``False``)
* :setting:`django:SESSION_COOKIE_AGE` (also available as a Control Panel setting, default: 2 weeks)


Site-related settings
~~~~~~~~~~~~~~~~~~~~~~~

.. _DOMAIN_REDIRECTS:

``DOMAIN_REDIRECTS``
~~~~~~~~~~~~~~~~~~~~

A list of domain names that will redirect to the site's primary domain name.

By default, this is populated by the Control Panel. If required, it can also be
specified as an environment variable on the Live server (recommended) or in
``settings.py``.

Setting this manually will allow you to add the internal Divio domain of the
site, such as ``example.eu.aldryn.io``, to the domains that will redirect to
the primary domain. (You may wish to do this if you don't want users or search
engines to discover your site at ``example.eu.aldryn.io`` rather than
``example.com``.)

Note that if you specify ``DOMAIN_REDIRECTS`` manually, you will need to list
all of its secondary domains, as it overrides the setting automatically
generated by the Control Panel.


.. _ALDRYN_SITES_REDIRECT_PERMANENT:

``ALDRYN_SITES_REDIRECT_PERMANENT``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, redirects are ``302 Temporary Redirect``. When ``True``, redirects
(where this is appropriate) will be ``301 Permanent Redirect``.

Can be specified as an environment variable (recommended) or in ``settings.py``.

See :ref:`301vs302` for more information.


Storage settings
~~~~~~~~~~~~~~~~

.. _static-file-cache-control:

Cache control for static files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Static files in our Django projects are collected by Django at build time, and served by uWSGI.
Aldryn Django configures the command it issues to uWSGI to start static file serving on the basis
of project settings. By default, files are served with no ``Cache-Control`` header applied.


.. _STATICFILES_DEFAULT_MAX_AGE:

``STATICFILES_DEFAULT_MAX_AGE``
...............................

The ``STATICFILES_DEFAULT_MAX_AGE`` determines the ``Cache-Control`` header value that uWSGI will
use for unhashed files (see the :ref:`hash-static-file-names` option, above). It is not recommended
to set this to high values, as the cached versions can continue to be used even after files
themselves have been updated.


.. _DISABLE_S3_MEDIA_HEADERS_UPDATE:

DISABLE_S3_MEDIA_HEADERS_UPDATE
...............................

Applications using Aldryn Django will update media file headers by running:

..  code-block:: python

    python manage.py aldryn_update_s3_media_headers

as a :ref:`release command <release-commands>`; this can be controlled with the ``DISABLE_S3_MEDIA_HEADERS_UPDATE``
environment variable. The ``aldryn_update_s3_media_headers`` command can cause excessively long deployment times on
very large media buckets, so setting this variable to ``True`` can avoid that.


Django server settings
~~~~~~~~~~~~~~~~~~~~~~

See notes on ``DJANGO_WEB_WORKERS``, ``DJANGO_WEB_MAX_REQUESTS``, ``DJANGO_WEB_TIMEOUT`` in
:ref:`How to fine-tune your server's performance <aldryn-django-performance-settings>`.


Email settings
~~~~~~~~~~~~~~

See :ref:`sending-email` for details of available settings.


Miscellaneous settings
~~~~~~~~~~~~~~~~~~~~~~

* ``DISABLE_GZIP`` determines whether Django's :mod:`GZipMiddleware
  <django:django.middleware.gzip>` will be added to the project's middleware (default: ``False``)
* :setting:`django:TIME_ZONE` (default: the appropriate time zone for your server region)
* ``SENTRY_DSN`` - if provided, logging to `Sentry <https://sentry.io>`_ will be configured
  automatically
