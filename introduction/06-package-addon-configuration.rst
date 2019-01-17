.. _tutorial-package-addon-configuration:

Package an addon (configuration)
================================

..  admonition:: This tutorial assumes your project uses Django 1.11

    At the time of writing, version 1.11 is `Django's Long-Term Support release
    <https://www.djangoproject.com/download/#supported-versions>`_, and is
    guaranteed support until at least April 2020.
    
    If you use a different version, you will need to modify some of the code
    examples and version numbers of packages mentioned.


There are a few more steps required. One feature of the Divio Cloud Control
Panel is the option to configure the settings associated with addons via a form.

The form is a fairly standard Django ``Form`` class. It needs to be built into
the addon, so that it will be exposed on the Control Panel.

This form also has a special method called ``to_settings()``, which is used to
manipulate the project's settings for the addon.

The form needs to be in a file called ``aldryn_config.py``, placed alongside
the other addon packaging files.


Add the addon to settings
-------------------------

..  note::

    This step will be performed automatically in a forthcoming update to the
    *Divio CLI* application when ``divio project develop`` is invoked.

Add the addon to the ``INSTALLED_ADDONS``, *inside* the ``<INSTALLED_ADDONS>``
tags:

..  code-block:: python
    :emphasize-lines: 7

    INSTALLED_ADDONS = [
        # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
        'aldryn-addons',
        'aldryn-django',
        'aldryn-sso',
        'aldryn-devsync',
        'tutorial-django-debug-toolbar',
        # </INSTALLED_ADDONS>
    ]

This adds the addon to the list of addons that the project will "watch".

..  note::

    The presence of the addon in this list is temporary, while you are
    developing locally. Remove it once you're done, and don't push it to the
    Cloud. It won't cause any harm, but it will be removed and could produce
    a Git conflict next time you pull.


Create an ``aldryn_config.py`` file
-----------------------------------

This file will do the "heavy lifting" of configuring the project for your
addon.

When a project is built, it checks each addon for ``aldryn_config.py``, and
calls its ``Form.to_settings()`` method to configure settings. *Every* addon on
the Cloud will therefore need, at minimum, an ``aldryn_config.py`` that
contains::

    from aldryn_client import forms


    class Form(forms.BaseForm):

        def to_settings(self, data, settings):
            return settings

Create that now, in your ``tutorial-django-debug-toolbar`` directory.

So far, it doesn't actually do anything, but we can see that it receives a
``settings`` argument, which will contain the project's settings that can we
then can manipulate and pass on.


Configure ``settings.py``
-------------------------

In ``settings.py`` we currently have:

..  code-block:: python

    if DEBUG:

        INSTALLED_APPS.extend(["debug_toolbar"])

        def _show_toolbar(request):
            return True

        DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": _show_toolbar}

        MIDDLEWARE_CLASSES.insert(
            MIDDLEWARE_CLASSES.index("django.middleware.gzip.GZipMiddleware") + 1,
            "debug_toolbar.middleware.DebugToolbarMiddleware"
        )

**Remove** all that from ``settings.py``. If you refresh your project's
admin page, you'll see the Debug Toolbar is no longer there.

We're going to implement those settings in the ``aldryn_config.py`` instead
(note that they're in a method now, so will look slightly different):

..  code-block:: python
    :emphasize-lines: 6,7, 11-20

    from aldryn_client import forms


    class Form(forms.BaseForm):

        def _show_toolbar(self, request):
            return True

        def to_settings(self, data, settings):

            if settings["DEBUG"]:

                settings["INSTALLED_APPS"].extend(["debug_toolbar"])

                settings["DEBUG_TOOLBAR_CONFIG"] = {"SHOW_TOOLBAR_CALLBACK": self._show_toolbar}

                settings["MIDDLEWARE_CLASSES"].insert(
                    settings["MIDDLEWARE_CLASSES"].index("django.middleware.gzip.GZipMiddleware") + 1,
                    "debug_toolbar.middleware.DebugToolbarMiddleware"
                )

            return settings

And if you refresh the admin, the Toolbar should be back.


Configure ``urls.py``
---------------------

The next step is to move the URLs configuration to the addon too.

Remove all the configuration related to Django Debug Toolbar from the project's
``urls.py``.

Check the admin - it should now raise a ``NoReverseMatch`` error, because it's
looking for ``djdt`` URLs that don't exist.

In ``tutorial_django_debug_toolbar`` (alongside the ``__init__.py``) add a
``urls.py``::

    from django.conf.urls import url, include

    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))]

Notice that this time we don't check for ``settings["DEBUG"]`` in the
``urls.py``. We can do it in the existing check, in the ``to_settings()`` method of ``aldryn_config.py``:

..  code-block:: python
    :emphasize-lines: 7

    def to_settings(self, data, settings):

        if settings["DEBUG"]:

            [...]

            settings['ADDON_URLS'].append('tutorial_django_debug_toolbar.urls')

        return settings

In the admin, the Toolbar should be working once more.

We now have *a self-configuring addon*, with only the most minimal traces of it
left in the project configuration itself.

The remaining steps are concerned with completing the configuration and
packaging of the addon for the Divio Cloud.

..  note::

    This configuration example in ``aldryn_config.py`` is somewhat simplified. For example,
    although ``GZipMiddleware`` is *probably* installed, that's not guaranteed. Our version will
    raise a ``ValueError`` if it's not. For a fuller, more robust version, see `the
    aldryn_config.py in the official Divio version of the addon
    <https://github.com/aldryn/aldryn-django-debug-toolbar/blob/master/aldryn_config.py>`_.
