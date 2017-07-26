.. _log-in-local-project:

Log in to a local Django project
=====================================

By default, Divio Cloud projects include the :ref:`divio-cloud-sso` addon.

This allows you to log in to any of your projects automatically (whether locally, on the test
environment or the live server) with your credentials provided to the Control Panel.

When you reach a log-in page locally, Aldryn SSO will offer you various options.

1. Create new Django super user.
#. Login with an existing user (if you've previously logged in on the Test server, your user will
   have been created automatically in the database).
#. Sign in with a Django user created for example with ``manage.py createsuperuser``.

..  image:: /images/log-in-local-project.png
    :alt: 'Options for local log-in'
