..  If this file moves, ensure that the redirect at divio.com/docs/settings is amended appropriately.

..  _settings.py:

The ``settings.py`` file
========================

Divio Cloud Django projects that use our addons framework are shipped with a ``settings.py`` file that hooks into the
framework. The framework allows addon applications to configure their own settings programmatically.

At first sight, this ``settings.py`` file may seem unusual, but in fact it behaves as a standard Django settings module.

``INSTALLED_ADDONS``
----------------------

The ``INSTALLED_ADDONS`` lists the addons installed by the addons framework. The list is populated automatically:

* on the Control Panel, when addons are added or removed
* locally, when the ``divio project develop`` command is run

Items are inserted between the ``<INSTALLED_ADDONS>`` tags. If you need to add items to the list manually while
developing, add them *outside* the tags, otherwise your changes will be overwritten the next time ``divio project
develop`` is run.

..  code-block:: python

    INSTALLED_ADDONS = [
        # <INSTALLED_ADDONS>
        ...
        # </INSTALLED_ADDONS>
    ]

Settings in Divio Cloud projects can either be configured automatically via the addons framework, or set
manually.


.. _addon-configured:

Setings that are configured by addons
--------------------------------------

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
    ``aldryn_addons.settings.load(locals())``, it may be overwritten by the addon system.

    If you declare it **after** ``aldryn_addons.settings.load(locals())``, it will overwrite any
    configuration performed by the addon system. In this case, your setting *will* apply, but be
    aware that logic in the addon's ``aldryn_config.py`` might operate based on a different value,
    with unpredictable results.


See :ref:`how-to-settings` for examples of how to handle these settings correctly.


.. _manually-configured:

Settings that are configured manually
-----------------------------------------

*Manually-configured* settings, that are not required or handled by any other component, can simply be dropped directly into your ``settings.py``.
