.. _django-manage-redirects:

How to manage redirects in Aldryn Django projects
==================================================

..  Seealso:: :ref:`domains`

.. _django_protocol_redirects:

Protocol redirects
------------------

Divio projects are HTTPS-ready by default, and we provide free SSL certificates on all projects.

To force redirect from HTTP to HTTPS in Django, set the :ref:`SECURE_SSL_REDIRECT <security-middleware-settings>`
environment variable to ``True``.


.. _domain_name_redirects:

Domain name redirects
---------------------

You can set up your site's domains using the `domains` section of the Control Panel. This includes the ability
to set a primary and secondary domains. The secondary domains can each be set to redirect to the primary domain if
required. You can enable / disable redirects from the three dots menu which will automatically populate ``DOMAIN``, ``DOMAIN_REDIRECTS`` and ``DOMAIN_ALIASES``.

Domain redirects can also be managed manually, via :ref:`DOMAIN_REDIRECTS` in the `env variables` section of the Control Panel. The list of domains is comma-separated. Note that doing this overrides all settings applied in the Control Panel - so if you use ``DOMAIN_REDIRECTS``, you will need to list **all** the domains there yourself.
Refer to :ref:`domain settings and environment variables <domain-settings-and-env-vars>` for more information.


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


Permanent redirects
-------------------

:ref:`ALDRYN_SITES_REDIRECT_PERMANENT` will force permanent redirects for protocol and domain directs. This is to be
:ref:`used with caution <301vs302>`.
