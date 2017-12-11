..  _settings.py:

The ``settings.py`` file
========================

Settings in Divio Cloud projects will either be configured by addons, or set
manually.


.. _addon-configured:

*Addon-configured* settings
---------------------------

Some settings, for example ``INSTALLED_APPS`` or ``MIDDLEWARE`` (``MIDDLEWARE_CLASSES`` in older
versions of Django) are *addon-configured* settings in Divio Cloud projects, managed by the `Aldryn
Addons framework <https://github.com/aldryn/aldryn-addons>`_.

This allows applications to configure themselves when they are installed; for example, if an addon
requires certain applications to be listed in ``INSTALLED_APPS``, it will add them (this is taken
care of in the addon's :ref:`configure-with-aldryn-config` file). All these are then loaded into the
``settings.py`` by the line::

    aldryn_addons.settings.load(locals())

..  important::

    If you declare a setting such as ``INSTALLED_APPS`` **before**
    ``aldryn_addons.settings.load(locals())``, it will be overwritten.

    If you declare it **after** ``aldryn_addons.settings.load(locals())``, it will overwrite the
    setting as configured by the addons.

    In either case, the settings **will not function correctly**.

See :ref:`how-to-settings` for examples of how to handle these settings correctly.


.. _manually-configured:

*Manually-configured* settings
---------------------------------

*Manually-configured* settings, that are not required or handled by any other component, are
much easier, and can simply be dropped directly into your ``settings.py``.
