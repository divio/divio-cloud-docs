.. _redirects:

Redirects
=========

You will find various redirects at work on URLs in Divio Cloud projects.

They fall into different categories:

* protocol redirects (e.g. ``http://example.com`` to ``https://example.com``)
* domain name redirects (e.g. ``https://example.com`` to ``https://www.example.com``)
* language redirects (e.g. ``https://example.com/about`` to ``https://example.com/en/about``)


Protocol redirects
------------------

Our projects are HTTPS-ready by default, and `we provide free SSL certificates even on free
projects <http://support.divio.com/control-panel/projects/ssl-certificates-and-https-on-divio-cloud-
projects>`_.

Adding a setting ``SECURE_SSL_REDIRECT`` (set to ``True``) (best done by using an environment
variable) will enable these redirects.

`SECURE_SSL_REDIRECT <https://docs.djangoproject.com/en/1.10/ref/settings/#secure-ssl-redirect>`_
is handled by the Django's ``SecurityMiddleware``.

By default, this is a ``302 Temporary Redirect``


Domain name redirects
---------------------

You can set up your site's domains using the `Domains section of the Control Panel
<http://support.divio.com/control-panel/projects/using-your-own-domain-with-divio-cloud>`_. This
includes the ability to set a primary and secondary domains. The secondary domains domains will
redirect to the primary domain.

By default, this is a ``302 Temporary Redirect``.


Language redirects
------------------

Django provides redirection to the the default language URL when none is specified. (In addition,
django CMS offers complex fallback options for unavailable languages.)

For example, ``/about`` will redirect to ``/en/about`` if English is the default language.

:ref:`Aldryn Django <aldryn-django>` can be configured to not use the prefix for the default
language, by checking the *Remove URL language prefix for default language* checkbox on the
settings for the Aldryn Django addon.

Alternatively, you can set ``PREFIX_DEFAULT_LANGUAGE`` to false in ``settings.py``.

Note that prior to version 1.10, this will not work with projects in which multiple languages
are defined.

This is a ``302 Temporary Redirect``.


301 Permanent and 302 Temporary redirects
-----------------------------------------

You will sometimes see online site-checking tools encouraging the use of permanent redirects and
even flagging temporary redirects as an issue. It is true that a permanent redirect is sometimes
more appropriate, but only when it really should be permanent, and is **guaranteed** not to change.


Protocol and domain directs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are ``302 Temporary`` by default. ``301 Permanent`` redirects are cached by browsers - some
even update their bookmarks if they encounter a ``301``. This can cause problems if the redirects
change, potentially causing redirect loops for users (which site owners will not be able to
replicate).

However, we do offer a setting (best provided by using an environment variable) to force permanent
redirects: ``ALDRYN_SITES_REDIRECT_PERMANENT=True``. This is to be used with caution.


Language redirects
^^^^^^^^^^^^^^^^^^

Language redirects are also temporary. This behaviour is determined in Django's core. It is not
safe to use permanent redirects here, because language redirects are content-dependent. A change in
the site could cause redirect loops, as described above, or spurious 404 errors.
