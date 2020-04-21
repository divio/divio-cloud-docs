.. _add-application:

How to add a new Django application to a project
================================================

..  note::

    This article assumes you are already familiar with the steps involved. For
    a full walk-through, see the :ref:`tutorial-add-applications` section of
    the :ref:`developer tutorial <introduction>`.

The recommended way of installing Django applications is to use a Divio Cloud
addon - an application that has already been packaged for easy installation in
our projects.

If an addon has not yet been created for the application you require, you have
two options:

* Add the application to the project manually (described in this article).
* Create an addon (described in :ref:`create-addon`).


Make the package available to the project
-----------------------------------------

You can do this in one of two ways:

* Copy the application to the root of the Python directory, so it's on the
  Python path.
* Add it to ``requirements.in``. See :ref:`install-python-dependencies` for
  details on how to do this.


Configure the project
---------------------

Configure settings
^^^^^^^^^^^^^^^^^^

Add the names of any required applications to the ``INSTALLED_APPS.extend()``
method in ``settings.py``.

Other key settings (such as ``MIDDLEWARE_CLASSES``) will already be defined in
settings, so **don't simply declare them** (e.g. ``MIDDLEWARE_CLASSES =
[...]``). If you do this, you will overwrite existing settings. Instead, use
for example ``MIDDLEWARE_CLASSES.extend([...])``.


Ordering of settings lists
..........................

The ordering of applications, middleware and other settings lists can matter,
in which case you may need to make sure you add the item at the start, end or
particular position in the list.

If for example your ``DebugToolbarMiddleware`` should be directly after the ``GZipMiddleware``, you could do:

..  code-block:: python

    MIDDLEWARE_CLASSES.insert(
        MIDDLEWARE_CLASSES.index("django.middleware.gzip.GZipMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware"
        )


Configure URLs
^^^^^^^^^^^^^^

Edit the ``urls.py`` of the project in the usual way, to include the ``urls.py`` of your application, for example:

..  code-block:: python
    :emphasize-lines: 2

    urlpatterns = [
        url(r'^polls/', include('polls.urls', namespace='polls')),
    ] + aldryn_addons.urls.patterns() + i18n_patterns(
        # add your own i18n patterns here
        *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
    )

Alternatively, add the URL configuration to be included via one of the
:ref:`addon URLs settings <addon-urls>`, in your project's ``settings.py``.


Migrate the database
--------------------

If the application has migrations, you should test them locally. Run:

..  code-block:: bash

    docker-compose run web python manage.py migrate


Deploy the project
------------------

Push your changes
^^^^^^^^^^^^^^^^^

..  code-block:: bash

    git add <changed or added files>
    git commit -m "<message describing what you did>"
    git push origin develop


Deploy the Test server
^^^^^^^^^^^^^^^^^^^^^^

..  code-block:: bash

    divio project deploy test
