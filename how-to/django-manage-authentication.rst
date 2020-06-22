.. _django-manage-access:

How to manage access authentication
===================================

In Django projects, access via password can be managed by the :ref:`Aldryn SSO addon <aldryn-sso>`.


.. _manage-access-login:

Require login
-------------------

By default, the Test site is password protected while the Live site is not. This is controlled by the
:ref:`ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN <ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN>` environment variable (``False`` for Test,
``True`` for Live).

To override the behaviour, you can set the value explictly in the *Environment variables* view in the Control Panel.


.. _password-protect-project:

Basic access authentication
-----------------------------------------

`.htaccess <https://en.wikipedia.org/wiki/.htaccess>`_ is a familiar way of
adding password protection to a web server at directory level.

Your Test server is always protected by our :ref:`SSO <aldryn-sso>`, but
you may occasionally require other forms of site-wide password protection.

It can be useful in the development process, for example, when you need to
restrict access, or for a site that provides API endpoints that should require
the client to authenticate.

A similar site-wide password requirement can be added to a Django site,
using environment variables. Set them as follows::

    ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN=basicauth
    ALDRYN_SSO_BASICAUTH_USER=<username>
    ALDRYN_SSO_BASICAUTH_PASSWORD=<password>

Those values can be set independently for test/live servers in the Environment
Variables settings for each project.

See :ref:`basic-auth` for more.
