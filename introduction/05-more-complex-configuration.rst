.. _tutorial-application-configuration:

Configure a more complex application
====================================

In the :ref:`previous section of the tutorial <tutorial-add-applications>`, we
added an application and deployed it. However, the installation process was extremely simple and
required very minimal configuration.

In practice, adding a Django application to a project will generally require more complex configuration.

We'll explore this by adding `Django Debug Toolbar
<https://django-debug-toolbar.readthedocs.io/en/stable/>`_ to the project.


Add django-debug-toolbar to ``requirements.in``
-----------------------------------------------

The `Django Debug Toolbar installation notes
<https://django-debug-toolbar.readthedocs.io/en/stable/installation.html>`_ suggest to install it using ``pip install
django-debug-toolbar``. The latest stable version at the time of writing is 2.2, so add ``django-debug-toolbar==2.2``
to ``requirements.in``.

:ref:`As before <tutorial-add-requirements>`, run ``docker-compose build web`` to rebuild the project with the new
requirement. Run ``docker-compose build web`` to rebuild the project with the new dependency.


Configure ``settings.py``
----------------------------

Django Debug Toolbar requires various settings to be configured. We don't want to load the Debug Toolbar into the
project unless we're running in with ``DEBUG = True`` (doing so could expose data and configuration that we definitely
should not share with the outside world.) So, in the configuration, we'll check for this.


Configure INSTALLED_APPS
^^^^^^^^^^^^^^^^^^^^^^^^

Debug Toolbar requires ``django.contrib.staticfiles`` and ``debug_toolbar`` to
be present in ``INSTALLED_APPS``. Is ``django.contrib.staticfiles`` already there? There's an easy way to check: run

..  code-block:: bash

    docker-compose run web python manage.py diffsettings

The Django :djadmin:`diffsettings <django:diffsettings>` management command shows the differences between your settings
and Django's defaults. In this case it should reassure us that ``django.contrib.staticfiles`` is already there as it's
included in Divio Django projects by default, so we just need to add ``debug_toolbar``:

..  code-block:: python

    if DEBUG:

        INSTALLED_APPS.extend(["debug_toolbar"])


Configure middleware settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`The installation documents note that we must set up the middleware
<https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#middleware>`_, and that it should come as soon
as possible in the list "after any other middleware that encodes the response’s content, such as ``GZipMiddleware``."

So let's insert it right after ``django.middleware.gzip.GZipMiddleware``:

..  code-block:: python
    :emphasize-lines: 5-8

    if DEBUG:

        INSTALLED_APPS.extend(["debug_toolbar"])

        MIDDLEWARE_CLASSES.insert(
            MIDDLEWARE_CLASSES.index("django.middleware.gzip.GZipMiddleware") + 1,
            "debug_toolbar.middleware.DebugToolbarMiddleware"
            )

This will find the ``GZipMiddleware`` in the list, and insert the ``DebugToolbarMiddleware`` immediately after it.


Triggering the toolbar
^^^^^^^^^^^^^^^^^^^^^^

The toolbar is only triggered if certain conditions are met. By default, it's only if ``DEBUG = True`` and the server
IP address is `listed in INTERNAL_IPS
<https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configuring-internal-ips>`_.

With Docker, we don't have a way to know what internal IP address a project will have, so we can't rely on that.
However, relying on ``DEBUG`` will be enough, so we define a function that will serve as a ``SHOW_TOOLBAR_CALLBACK``
callback to replace the default:

..  code-block:: python

    def show_toolbar(request):
        return DEBUG

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}


Configure ``urls.py``
---------------------

We need to include the ``debug_toolbar.urls`` in the project's URL configuration. Our approach in the ``urls.py`` is
similar: we only want it active in ``DEBUG`` mode, so this to the end of the file:

..  code-block:: python

    from django.conf import settings

    if settings.DEBUG:
        from django.urls import include, path
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns


See the results
---------------

And that's it (Debug Toolbar has no database tables, so you don't need to run
migrations).

Visit the admin to see the Debug Toolbar in action.

.. image:: /images/intro-debug-toolbar.png
   :alt: 'Django Debug Toolbar'

