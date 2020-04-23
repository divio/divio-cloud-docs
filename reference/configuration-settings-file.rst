..  This section is referred to (as https://docs.divio.com/en/latest/how-to/configure-settings.html) from
    within the settings.py file provided by standard Aldryn Django projects. Do not change this reference.

..  _settings.py:

The ``settings.py`` file
========================

Divio Django projects that use our addons framework are shipped with a ``settings.py`` file that hooks into the
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

Settings in Divio Cloud projects can either be :ref:`configured automatically via the addons framework
<application-configuration>`, or set manually.


Automatic settings loading
--------------------------

Using this list of ``INSTALLED_ADDONS``, the::

  import aldryn_addons.settings
  aldryn_addons.settings.load(locals())

section that follows checks each one for any settings that it has to apply. These settings will be loaded into the
settings module at this point. For example, ``INSTALLED_APPS`` will be populated appropriately.

Any settings that have been loaded can be manipulated. For example, to add new applications to ``INSTALLED_APPS``,
you can add them in::

  INSTALLED_APPS.extend([
      # Extend the INSTALLED_APPS setting by listing additional applications here
  ])

It's important to understand which settings are applied automatically.

If you declare a setting such as ``INSTALLED_APPS`` **before** ``aldryn_addons.settings.load(locals())``, it may be
overwritten by the addon system.

If you declare it **after** ``aldryn_addons.settings.load(locals())``, it will overwrite any configuration performed by
the addon system, with possibly unpredictable results.

See :ref:`application-configuration` for an overview of how settings are handled in general, and :ref:`how-to-settings`
for advice on how to manipulate them.
