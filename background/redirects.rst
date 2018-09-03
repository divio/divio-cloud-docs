.. _redirects:

Redirects
=========

You will find various redirects at work on URLs in Divio Cloud projects.

They fall into different categories:

* :ref:`protocol_redirects` (e.g. from HTTP to HTTPS)
* :ref:`domain_name_redirects` (e.g. ``https://example.com`` to
  ``https://www.example.com``)
* :ref:`language_redirects` (e.g. ``https://example.com/about`` to
  ``https://example.com/en/about``)

All are by default ``302 Temporary Redirects``.


.. _protocol_redirects:

Protocol redirects
------------------

Our projects are HTTPS-ready by default, and `we provide free SSL certificates
even on free projects
<http://support.divio.com/control-panel/projects/ssl-certificates-and-https-on-divio-cloud- projects>`_.

Adding a :ref:`SECURE_SSL_REDIRECT` will enable these redirects.


.. _domain_name_redirects:

Domain name redirects
---------------------

You can set up your site's domains using the `Domains section of the Control
Panel
<http://support.divio.com/control-panel/projects/using-your-own-domain-with-divi
o-cloud>`_. This includes the ability to set a primary and secondary domains.
The secondary domains can each be set to redirect to the primary domain if
required.

The domains that are to be redirected to the primary domain can also be managed
manually, via :ref:`DOMAIN_REDIRECTS`.


.. _language_redirects:

Language redirects
------------------

Django provides redirection to the the default language URL when none is
specified. (In addition, django CMS offers complex fallback options for
unavailable languages.)

For example, ``/about`` will redirect to ``/en/about`` if English is the
default language.

:ref:`aldryn-django <aldryn-django>` can be configured to not use the prefix
for the default language, by checking the :ref:`Remove URL language prefix for
default language <PREFIX_DEFAULT_LANGUAGE>` checkbox on the settings for the
Aldryn Django addon in the Control Panel.


.. _301vs302:

301 Permanent vs 302 Temporary redirects
----------------------------------------

You will sometimes see online site-checking tools encouraging the use of
permanent redirects and even flagging temporary redirects as an issue. It is
true that a permanent redirect is sometimes more appropriate, but only when it
really should be permanent, and is **guaranteed** not to change.

Protocol, domain and language directs are ``302 Temporary`` by default. ``301
Permanent`` redirects are cached by browsers - some even update their bookmarks
if they encounter a ``301``. This can cause problems if the redirects change,
potentially causing redirect loops for users (which site owners will not be
able to replicate).

However, we do offer a setting :ref:`ALDRYN_SITES_REDIRECT_PERMANENT` to force
permanent redirects for protocol and domain directs. This is to be used with
caution.
