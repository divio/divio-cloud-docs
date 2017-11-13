.. _aldryn-django:

Aldryn Django (core Django)
===========================

Aldryn Django (``aldryn-django``) installs and provides basic configuration for Django.


Key Aldryn Django configuration options
---------------------------------------

.. _PREFIX_DEFAULT_LANGUAGE:

*Remove URL language prefix for default language*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set on the Aldryn Django configuration on the Control Panel.

When set, will remove ``django.middleware.locale.LocaleMiddleware`` from the
middleware.

This will cause Django not to use a language prefix in the URL when serving the
default language. For example, ``/about`` will redirect to ``/en/about`` if
English is the default language.

Note that prior to version 1.10, this will not work with projects in which
multiple languages are defined.

This is a ``302 Temporary Redirect``, as determined in Django's core. It is not
safe to use permanent redirects here, because language redirects are
content-dependent. A change in the site could cause redirect loops, as
described above, or spurious 404 errors.


.. _SECURE_SSL_REDIRECT:

``SECURE_SSL_REDIRECT``
~~~~~~~~~~~~~~~~~~~~~~~

When ``True``, redirects to the HTTPS version of the site.

Can be specified as an environment variable (recommended) or in ``settings.py``.

The `SECURE_SSL_REDIRECT setting
<https://docs.djangoproject.com/en/1.10/ref/settings/#secure-ssl-redirect>`_ is
handled by Django's ``SecurityMiddleware``.

By default, this is a ``302 Temporary Redirect``


.. _ALDRYN_SITES_REDIRECT_PERMANENT:

ALDRYN_SITES_REDIRECT_PERMANENT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, redirects are ``302 Temporary Redirect``. When ``True``, redirects
(where this is appropriate) will be ``301 Permanent Redirect``.

Can be specified as an environment variable (recommended) or in ``settings.py``.

See :ref:`301vs302` for more information.


Other options
-------------

See `aldryn-django.aldryn_config
<https://github.com/aldryn/aldryn-django/blob/support/1.8.x/aldryn_config.py>`_
for the settings it takes and how they are applied. (Check that you are
referring to the appropriate version.)

