.. _special-settings:

Special Divio Cloud project settings
====================================

A Divio Cloud project has a number of special settings that can be used for
particular purposes:


.. _addon-urls:

Addon URLs
    Divio Cloud offers four different ways of specifying URL patterns for
    insertion into a project’s ``urls.py`` .

    * ``ADDON_URLS``  to insert them
    * ``ADDON_URLS_LAST`` to insert them in last place
    * ``ADDON_URLS_I18N`` to insert them as ``i18n_patterns`` (i.e. translatable
      URL patterns)
    * ``ADDON_URLS_I18N_LAST`` to insert them after the other translatable URL
      patterns

    Example::

        ADDON_URLS_I18N = 'django_example_utilities.urls'
