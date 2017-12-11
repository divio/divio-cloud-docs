..  _how-to-settings:

How to configure Django settings
================================

It is important to understand that in Divio Cloud projects, some settings need to be inspected and
manipulate programatically, to allow the addons system to handle configuration automatically. See
the :ref:`addon-configured` section for more on this.

This can entail a little extra work when you need to change settings yourself, but the huge
convenience it offers is more than worth the effort.

The correct way to manage settings such as ``INSTALLED_APPS`` is to manipulate the existing value,
after having loaded the settings from the addons with ``aldryn_addons.settings.load(locals())``.
For example, in the default ``settings.py`` you will find::

    import aldryn_addons.settings
    aldryn_addons.settings.load(locals())

    INSTALLED_APPS.extend([
        # add your project specific apps here
    ])

This allows you to add items to ``INSTALLED_APPS`` without overwriting existing items, by
manipulating the list.

You will need to do the same for other configured settings, which will include:

* ``MIDDLEWARE`` (or the older ``MIDDLEWARE_CLASSES``)
* ``TEMPLATES`` (or the older ``TEMPLATE_CONTEXT_PROCESSORS``, ``TEMPLATE_DEBUG`` and other
  template settings)
* application-specific settings, for example that belong to django CMS or Wagtail. See each
  application's :ref:`configure-with-aldryn-config` for the settings it will configure.


Inserting an item at a particular position
------------------------------------------

Sometimes it's not enough just to *add* an application or class to a list. It may need to be
added before another item. Say you need to add your application `security` just before `cms`. In this case you can target `cms` in the list like this::

    INSTALLED_APPS.insert(
        INSTALLED_APPS.index("cms") + 0,
        "security"
    )

(``+ 0`` will insert the new item ``"security"`` immediately before ``"cms"`` in the list).

Of course you can use Python to manipulate the collections in any way you require.


Manipulating more complex settings
----------------------------------

Note that in the case of more complex settings, like ``MIDDLEWARE`` or ``TEMPLATES``, which are no
longer simple lists, you can't just extend them directly with new items, you'll need to dive into
them to target the right list in the right dictionary, for example::

     TEMPLATES[0]["OPTIONS"]["context_processors"].append('my_application.some_context_processor')
