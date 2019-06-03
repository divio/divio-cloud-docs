.. _aldryn-addons:

Aldryn Addons (addon integration)
====================================

The Aldryn Addons framework helps integrate addons and their settings into
a Django project.

It's an `open-source package <https://github.com/aldryn/aldryn-addons/>`_, and
is itself an addon. The addons framework is installed by default in all Divio
Cloud Django projects.


Aldryn Addons configuration options
-----------------------------------

.. _addon-urls:

Addon URLs
~~~~~~~~~~

A project, or an addon in it, may need to specify some URL patterns.

They could simply be added to the project's ``urls.py`` manually. However, it's
also convenient for addons to be able to configure URLs programmatically, so
that when an addon is installed, it will also take care of setting up the
relevant URL configurations.

Aldryn Addons provides a way to do this. A Divio Cloud project's ``urls.py``
contains::

    urlpatterns = [
        # add your own patterns here
    ] + aldryn_addons.urls.patterns() + i18n_patterns(
        # add your own i18n patterns here
        *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
    )

As well as indicated places for manually-added patterns, it calls
``aldryn_addons.urls.patterns()`` and ``aldryn_addons.urls.i18n_patterns()``.

These functions, in `the urls.py of Aldryn Addons
<https://github.com/aldryn/aldryn-addons/blob/master/aldryn_addons/urls.py>`_,
check for and return the values in four different settings:


``ADDON_URLS`` and ``ADDON_URLS_I18N``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are expected to be lists of URL patterns. Each addon that needs to add
its own URL patterns should add them to the lists.

For example, in `Aldryn django CMS
<https://github.com/aldryn/aldryn-django-cms/blob/support/3.4.x/aldryn_config.py>`_::

    settings['ADDON_URLS'].append('aldryn_django_cms.urls')


``ADDON_URLS_LAST`` and ``ADDON_URLS_I18N_LAST``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are not lists, and only one of each can be set in any project - it's not
possible for two applications both to specify an ``ADDON_URLS_I18N_LAST`` for
example.

django CMS sets ``settings['ADDON_URLS_I18N_LAST'] = 'cms.urls'`` - so in
a project using django CMS, no other application can use ``ADDON_URLS_I18N_LAST``.
