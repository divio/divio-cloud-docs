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
``settings.py`` by its::

    aldryn_addons.settings.load(locals())

..  important::

    If you declare a setting such as ``INSTALLED_APPS`` **before**
    ``aldryn_addons.settings.load(locals())``, it will be overwritten.

    If you declare it **after** ``aldryn_addons.settings.load(locals())``, it will overwrite the
    setting as configured by the addons.

    In either case, the settings **will not function correctly**.

The correct way to manage settings such as ``INSTALLED_APPS`` is to manipulate the existing value, after having loaded the settings from the addons with ``aldryn_addons.settings.load(locals())``.
For example, in the default ``settings.py``::

    import aldryn_addons.settings
    aldryn_addons.settings.load(locals())

    INSTALLED_APPS.extend([
        # add your project specific apps here
    ])

so you can add items to ``INSTALLED_APPS`` without overwriting existing items, by manipulating the
list.

You will need to do the same for other configured settings, which will include:

* ``MIDDLEWARE`` (or the older ``MIDDLEWARE_CLASSES``)
* ``TEMPLATES`` (or the older ``TEMPLATE_CONTEXT_PROCESSORS``, ``TEMPLATE_DEBUG`` and other
  template settings)
* application-specific settings, for example that belong to django CMS or Wagtail. See each
  application's :ref:`configure-with-aldryn-config` for the settings it will configure.

Note that in the case of more complex settings, like ``MIDDLEWARE`` or ``TEMPLATES``, which are no
longer simple lists, you can't just extend them directly with new items, you'll need to dive into
them to target the right list in the right dictionary, for example::

     TEMPLATES[0]["OPTIONS"]["context_processors"].append('my_application.some_context_processor')


.. _manually-configured:

*Manually-configured* settings
---------------------------------

*Manually-configured* settings, that are not required or handled by any other component, are
much easier, and can simply be dropped directly into your ``settings.py``.
