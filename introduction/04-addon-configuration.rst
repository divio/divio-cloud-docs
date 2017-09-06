.. tutorial-application-configuration:

Configure an application
========================

In the :ref:`previous section of the tutorial <tutorial-add-applications>`, we
added a couple of applications. However, they were extremely simple and
required very minimal configuration in the project's ``settings.py`` and
``urls.py``. In practice, adding a Django application to a project will require
more complex configuration.

We'll explore this by adding `Django Debug Toolbar
<https://django-debug-toolbar.readthedocs.io/en/stable/>`_ to the project.


..  note::

    At this stage we will assume that you have your project running locally. See
    :ref:`tutorial-control` for a refresher on how to control your project.

    For these steps, running your project with::

        docker-compose run --rm --service-ports web python manage.py runserver 0.0.0.0:80

    is a good way of monitoring progress.


Add django-debug-toolbar to requirements.in
-------------------------------------------

The `Django Debug Toolbar installation notes
<https://django-debug-toolbar.readthedocs.io/en/stable/installation.html>`_
suggest to install it using ``pip install django-debug-toolbar``.

The latest stable version at the time of writing is 1.8, so add
``django-debug-toolbar==1.8`` to ``requirements.in``:

..  code-block:: python
    :emphasize-lines: 5

    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    [...]
    # </INSTALLED_ADDONS>
    django-axes==2.3.2
    django-debug-toolbar==1.8

Run ``docker-compose build web`` to rebuild the project with the new
requirement.


Configure ``settings.py``
----------------------------

We want Django Debug Toolbar to be active *only* when running with ``DEBUG =
True``, so all configuration for it will be conditional on an ``if DEBUG`` test.

Configure INSTALLED_APPS
^^^^^^^^^^^^^^^^^^^^^^^^

Debug Toolbar requires ``django.contrib.staticfiles`` and ``debug_toolbar`` to
be present in ``INSTALLED_APPS``. ``django.contrib.staticfiles`` is installed
in Divio Cloud projects by default, so we just add ``debug_toolbar``:

..  code-block:: python

    if DEBUG:

        INSTALLED_APPS.extend(["debug_toolbar"])


Configure Debug Toolbar settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Normally, you'd set `INTERNAL_IPS
<https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#interna
l-ips>`_ to ensure that this only runs on certain servers. With Docker, we
don't always know what internal IP address a project will have, so we can't
rely on that. However, relying on ``DEBUG`` will be enough, so we define
a function that will serve as a ``SHOW_TOOLBAR_CALLBACK`` callback to replace
the default:

..  code-block:: python
    :emphasize-lines: 5-8

    if DEBUG:

        [...]

        def _show_toolbar(request):
            return True

        DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": _show_toolbar}


Configure middleware settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`The installation documents note that we must set up the middleware
<https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#middleware>`_, and that it should come as soon as possible in the list "after any
other middleware that encodes the response’s content, such as GZipMiddleware."

So let's insert it right after ``django.middleware.gzip.GZipMiddleware``:

..  code-block:: python
    :emphasize-lines: 5-8

    if DEBUG:

        [...]

        MIDDLEWARE_CLASSES.insert(
            MIDDLEWARE_CLASSES.index("django.middleware.gzip.GZipMiddleware") + 1,
            "debug_toolbar.middleware.DebugToolbarMiddleware"
            )


Configure ``urls.py``
---------------------

Our approach in the ``urls.py`` is similar: we only want it active in ``DEBUG``
mode:

..  code-block:: python
    :emphasize-lines: 1, 5-9

    from django.conf import settings

    [...]

    if settings.DEBUG:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns


See the results
---------------

And that's it (Debug Toolbar has no database tables, so you don't need to run
migrations).

Visit the admin to see the Debug Toolbar in action.

.. image:: /images/debug-toolbar.png
   :alt: 'Django Debug Toolbar'

