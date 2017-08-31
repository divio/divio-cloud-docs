.. _key-addons:

Key Divio Cloud project addons
==============================

A number of addons provide important basic functionality in Divio Cloud
projects.

In the ``aldryn_config.py`` of these addons you'll find many useful insights
into how they configure themselves, and the settings they apply. See the
:ref:`notes on aldryn_config.py <aldryn-config>` to understand the significance
of this file.


.. _aldryn-django:

``aldryn-django`` (our default Django set-up)
---------------------------------------------

``aldryn-django`` installs and provides basic configuration for Django.

See `aldryn-django.aldryn_config
<https://github.com/aldryn/aldryn-django/blob/support/1.8.x/aldryn_config.py>`_
for the settings it takes and how they are applied.


.. _divio-cloud-sso:

``aldryn-sso`` (Divio Cloud single-sign-on)
-------------------------------------------

The Divio Cloud SSO (single-sign-on) system provides a convenient way to authenticate users for
Divio Cloud projects (whether locally, or on the Test or Live servers) without needing to log in
again, as long as they have logged into the Divio Cloud Control Panel.

This includes making it possible for users working on projects locally to
log in locally with a single click, as they have already been authenticated.

Divio Cloud SSO is managed by the `aldryn-sso
<https://github.com/aldryn/aldryn-sso>`_ package.


Key options in ``aldryn-sso``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN``
    Options:

    * ``True``: Users cannot view the site without logging in. This is the default for the *Test*
      server.
    * ``False``: Anonymous users may view the site.
    * ``basicauth``: Set up `basic HTTPS authentication <https://en.wikipedia.org/wiki/Basic_access_authentication>`_.

``ALDRYN_SSO_BASICAUTH_USER``, ``ALDRYN_SSO_BASICAUTH_PASSWORD``
    Required when ``basicauth`` is enabled.

See its `aldryn-sso.aldryn_config.py
<https://github.com/aldryn/aldryn-sso/blob/master/aldryn_config.py>`_ for
other settings it takes and how they are applied.



..  todo::

    Other addons:

    * dev-sync - allows desktop client to sync changes
    * aldryn-sites - domain settings
