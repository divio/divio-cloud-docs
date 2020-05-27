.. _password-protect-project:

How to set up project-wide password protection
==============================================

`.htaccess <https://en.wikipedia.org/wiki/.htaccess>`_ is a familiar way of
adding password protection to a web server at directory level.

Your Test server is always protected by our :ref:`SSO <authentication>`, but
you may occasionally require other forms of site-wide password protection.

It can be useful in the development process, for example, when you need to
restrict access, or for a site that provides API endpoints that should require
the client to authenticate.

A similar site-wide password requirement can be added to a Divio site,
using environment variables. Set them as follows::

    ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN=basicauth
    ALDRYN_SSO_BASICAUTH_USER=<username>
    ALDRYN_SSO_BASICAUTH_PASSWORD=<password>

Those values can be set independently for test/live servers in the Environment
Variables settings for each project.

See :ref:`basic-auth` for more.


How this works
--------------

These variables are handled in the :ref:`divio-cloud-sso` module.

You can see exactly what it does with them - and others - in
https://github.com/aldryn/aldryn-sso/blob/master/aldryn_config.py
