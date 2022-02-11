===========
Key addons
===========

.. _aldryn-django:

Aldryn Django (core Django)
===========================

..  note:: Aldryn continues to be supported by Divio, but we do not recommend using Aldryn Django for new applications.

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

For local development you will need to edit ``docker-compose.yml``, changing ``postgres:13.5-alpine`` to
``mdillon/postgis:13.5-alpine``. On the cloud, you will need to make a support request to have the new
database enabled for the project.

See :ref:`manage_postgres_extensions` for more details.


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

..  warning::

    Note that if you specify ``DOMAIN_REDIRECTS`` manually, you will need to list **all** the secondary domains you
    want to handle, as it overrides the setting automatically generated by the Control Panel.


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


.. _aldryn-sso:

Aldryn SSO (authentication)
==============================

..  note:: Aldryn continues to be supported by Divio, but we do not recommend using Aldryn Django for new applications.

Authentication to the Divio platform, and (by default) to user projects
running on the platform, is handled by the Divio SSO (single-sign-on)
system. This provides a convenient way to authenticate users for Divio
projects (whether locally, or on the *Test* or *Live* servers) without needing
to log in again, as long as they have logged into the Divio Control Panel.

This includes making it possible for users working on projects locally to
log in locally with a single click, as they have already been authenticated.

Divio SSO is managed by the `open-source Aldryn SSO
<https://github.com/aldryn/aldryn-sso>`_ addon. The system is optional, but is
installed by default in all Divio Django projects.

If the addon is uninstalled, then Django's standard authentication behaviour
will apply.


.. _login-methods:

Login methods
-------------

The Aldryn SSO addon provides three different login methods to Divio projects:

..  image:: /images/login-options.png
    :alt: 'Illustration of Divio project login options'
    :width: 552

Depending on how the project is configured, and which environment
(local/test/live) it's running in, different combinations of these options will
be shown (you'll never see all three at once in a real project).

The illustrated options are:

.. _local-development-login:

1. Local development login
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is intended to appear on locally-running projects only. The *Add user*
option is a convenient way to add new users to a project.

See :ref:`ALDRYN_SSO_ENABLE_LOCALDEV`.


.. _django-login-form:

2. Django's standard username/password login form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will not be of any use unless users with passwords exist in the database.

See :ref:`ALDRYN_SSO_ENABLE_LOGIN_FORM`.


.. _divio-cloud-sso:

3. Divio single-sign-on
~~~~~~~~~~~~~~~~~~~~~~~

This is intended to appear on projects running in Cloud environments only. It
allows users to sign in to their own projects with a single click, once they
have authenticated with the Divio control panel.

See :ref:`ALDRYN_SSO_ENABLE_SSO_LOGIN`.


Test site protection
--------------------

By default the *Test* site is protected so that it's not publicly discoverable
or viewable. Only the owner or an authorised user of the project can view its contents.

This is controlled with the :ref:`ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN` environment variable, which is `True` by default and
can be overridden by setting it manually.

See also :ref:`how to apply/remove password protection to Django sites <manage-access-login>`.


Aldryn SSO configuration options
--------------------------------

..  important::

    The preferred way to set these options is as environment variables.

    If you supply them as Django settings declared in :ref:`settings.py <settings.py>`, they must appear **before**
    ``aldryn_addons.settings.load(locals())``. This allows them to be processed correctly by the addons system.

    The exception is :ref:`ALDRYN_SSO_HIDE_USER_MANAGEMENT`, which is configured via the Control Panel, or by adding the
    variable *after* ``aldryn_addons.settings.load(locals())``.

More details of how Aldryn SSO processes these settings can be studied at
`aldryn-sso.aldryn_config.py
<https://github.com/aldryn/aldryn-sso/blob/master/aldryn_config.py>`_.


.. _ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN:

``ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Controls whether visitors need to be logged-in. Available options are:

* ``True``: Users will need to log in via the SSO system in order to access
  the site (default for test site).
* ``False``: No login is required (default for local and live environments).
* ``basicauth``: The site will be protected by `basic HTML access
  authorisation
  <https://en.wikipedia.org/wiki/Basic_access_authentication>`_. See
  :ref:`basicauth <basic-auth>`.

Can also be specified as an environment variable or in ``settings.py``.


.. _ALDRYN_SSO_ENABLE_LOCALDEV:

``ALDRYN_SSO_ENABLE_LOCALDEV``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enables :ref:`Local development login <local-development-login>`.

When ``True`` (default for the local environment only) enables the *Add user*
pane in the login form, providing a convenient way to add a new user to the
database.

Can also be specified as an environment variable or in ``settings.py``.

..  warning::

    For obvious reasons, enabling this is strongly not recommended on the
    *Test* and *Live* sites, and there is generally no good reason to
    manipulate this setting.


.. _ALDRYN_SSO_ENABLE_SSO_LOGIN:

``ALDRYN_SSO_ENABLE_SSO_LOGIN``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enables :ref:`single-sign-on <divio-cloud-sso>`.

Requires a value to be present in :ref:`SSO_DSN`, and is automatically set when
there is. If enabled when no ``SSO_DSN`` value has been set, an error will be
raised.

Can also be specified as an environment variable or in ``settings.py``.


.. _ALDRYN_SSO_ENABLE_LOGIN_FORM:

``ALDRYN_SSO_ENABLE_LOGIN_FORM``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enables :ref:`Django's standard username/password login form
<django-login-form>`.

By default, is enabled when :ref:`Hide user management
<ALDRYN_SSO_HIDE_USER_MANAGEMENT>` is **not** enabled.

Can also be specified as an environment variable or in ``settings.py``.


.. _ALDRYN_SSO_ENABLE_AUTO_SSO_LOGIN:

``ALDRYN_SSO_ENABLE_AUTO_SSO_LOGIN``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When ``True`` (the default on all sites) then if SSO login is the only login
method enabled, the user will be automatically logged-in via SSO (assuming of
course that the user is authorised to do so).

The logic for this condition is:

====================================  =========
ALDRYN_SSO_ENABLE_SSO_LOGIN           True
ALDRYN_SSO_ENABLE_AUTO_SSO_LOGIN      True
ALDRYN_SSO_ENABLE_LOGIN_FORM          False
ALDRYN_SSO_ENABLE_LOCALDEV            False
====================================  =========

Can also be specified as an environment variable or in ``settings.py``.


.. _ALDRYN_SSO_HIDE_USER_MANAGEMENT:

``ALDRYN_SSO_HIDE_USER_MANAGEMENT``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This option is presented in the configuration form for the Aldryn SSO addon on
the Control Panel (as *Hide user management*). Its effect is to unregister the
``User`` and ``Group`` models in the Django admin.

Setting it as an environment variable will have no effect.

Specifying it in `settings.py` will only have an effect if it is declared
*after* ``aldryn_addons.settings.load(locals())``. This is not recommended
except for testing purposes.

For local testing, the ``hide_user_management`` value in
``aldryn-addons/aldryn-sso/settings.json`` can be changed, mimicking the
effect of the form value.


.. _basic-auth:

Basic access authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic access authentication is configured using ``ALDRYN_SSO_BASICAUTH_USER`` and ``ALDRYN_SSO_BASICAUTH_PASSWORD``.

When ``ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN`` is set to ``basicauth``, access to
the entire site will require user and password details. This is an *additional
layer* of authentication. Access to the admin will still require login by an admin user, and even a logged-in admin user will need to supply the username
and password.

..  seealso::

    :ref:`password-protect-project`.

Though the username and password can be specified as an environment variable or
in ``settings.py``, the latter is not good practice.


.. _SSO_DSN:

``SSO_DSN``
~~~~~~~~~~~

The Data Source Name for single-sign-on.

This is set as an environment variable automatically in Cloud Projects,
adding the SSO authority to the URL configuration for the project.

If you are providing your own single-sign-on, ``SSO_DSN`` can also be specified
as an environment variable or in ``settings.py``.


``LOGIN_REDIRECT_URL``
~~~~~~~~~~~~~~~~~~~~~~

After login, redirect to the specified URL (by default, to ``/``).

Specifying ``LOGIN_REDIRECT_URL`` in `settings.py` will only have an effect if
it is declared *after* ``aldryn_addons.settings.load(locals())``.


``ALDRYN_SSO_LOGIN_WHITE_LIST``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of internal endpoints that don't require authentication. Defaults to an
empty list.

For example::

    from django.core.urlresolvers import reverse_lazy

    ALDRYN_SSO_LOGIN_WHITE_LIST = [reverse_lazy('my_whitelisted_endpoint')]

Can be specified as an environment variable or in ``settings.py``, or
manipulated programmatically in other applications::

    if 'ALDRYN_SSO_LOGIN_WHITE_LIST' in settings:

        settings['ALDRYN_SSO_LOGIN_WHITE_LIST'].extend([reverse_lazy('my_whitelisted_endpoint')])


``ALDRYN_SSO_OVERIDE_ADMIN_LOGIN_VIEW``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We override Django's admin login view by default, as long as one of the
:ref:`three login options <login-methods>` is enabled. This takes better care
of logged-in users who are not staff (admin) users.

The standard Django administration login view is available by setting this to
``False`` as an environment variable or in ``settings.py``.


.. _aldryn-addons:

Aldryn Addons (addon integration)
=================================

..  note:: Aldryn continues to be supported by Divio, but we do not recommend using Aldryn Django for new applications.

The Aldryn Addons framework helps integrate addons and their settings into
a Django project.

It's an `open-source package <https://github.com/aldryn/aldryn-addons/>`_, and
is itself an addon. The addons framework is installed by default in all Divio
Cloud Django projects.


Aldryn Addons configuration options
-----------------------------------

.. _addon-urls:

Addon URLs
~~~~~~~~~~

A project, or an addon in it, may need to specify some URL patterns.

They could simply be added to the project's ``urls.py`` manually. However, it's
also convenient for addons to be able to configure URLs programmatically, so
that when an addon is installed, it will also take care of setting up the
relevant URL configurations.

Aldryn Addons provides a way to do this. A Divio project's ``urls.py``
contains::

    urlpatterns = [
        # add your own patterns here
    ] + aldryn_addons.urls.patterns() + i18n_patterns(
        # add your own i18n patterns here
        *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
    )

As well as indicated places for manually-added patterns, it calls
``aldryn_addons.urls.patterns()`` and ``aldryn_addons.urls.i18n_patterns()``.

These functions, in `the urls.py of Aldryn Addons
<https://github.com/aldryn/aldryn-addons/blob/master/aldryn_addons/urls.py>`_,
check for and return the values in four different settings:


``ADDON_URLS`` and ``ADDON_URLS_I18N``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are expected to be lists of URL patterns. Each addon that needs to add
its own URL patterns should add them to the lists.

For example, in `Aldryn django CMS
<https://github.com/aldryn/aldryn-django-cms/blob/support/3.4.x/aldryn_config.py>`_::

    settings['ADDON_URLS'].append('aldryn_django_cms.urls')


``ADDON_URLS_LAST`` and ``ADDON_URLS_I18N_LAST``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are not lists, and only one of each can be set in any project - it's not
possible for two applications both to specify an ``ADDON_URLS_I18N_LAST`` for
example.

django CMS sets ``settings['ADDON_URLS_I18N_LAST'] = 'cms.urls'`` - so in
a project using django CMS, no other application can use ``ADDON_URLS_I18N_LAST``.
