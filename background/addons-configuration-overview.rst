.. _application-configuration:

How settings are handled in Django addons
=========================================

In Django projects, settings are handled via the :doc:`settings <django:topics/settings>` module (usually, the
``settings.py`` file).

In Aldryn addons - those that include an ``aldryn_config.py`` file - many of these settings will be automatically
managed by the addon itself. This takes place in ``aldryn_config.py``.

All key settings (i.e. settings required for the package to function correctly) as well as many optional settings will
be configured. They are then applied to the settings module via the lines::

 import aldryn_addons.settings
 aldryn_addons.settings.load(locals())

From this point in the settings module, those settings that were automatically configured by the addon will be available
in the ``settings.py`` file. For example, the project's ``addons/aldryn-django/aldryn_config.py`` will add entries to
``INSTALLED_APPS``, ``MIDDLEWARE`` and so on. Such settings can be controlled and determined in a number of ways.


Via Addon settings in the Control Panel
---------------------------------------

An Addon can expose options for configuration in the Control Panel interface. For example, Aldryn Django has a
:ref:`PREFIX_DEFAULT_LANGUAGE` option. This will apply to all cloud environments of the project. For the local
development environment, it will be placed in the project's ``addons/aldryn-django/settings.json``.


Via environment variables
--------------------------

Environment variables are suitable for:

* environment-specific settings (e.g. database settings, since each environment should have its own)
* secret settings (e.g. keys for services and APIs)

Environment variables are better for such settings than committing them to code because. If stored as part of the
codebase, they provide the same value in all environments, and they are vulnerable to being accidentally shared.


Via automatically applied environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some environment variables are provided automatically, and you don't need to do anything about them at all.

Each project environment has its own variables provided for services such as the database (``DEFAULT_DATABASE_DSN``), media storage (``DEFAULT_STORAGE_DSN``) and so on. Locally, the variables are saved in the ``.env-local`` file and :ref:`loaded into the environment via docker compose <docker-compose-env>`.


Via user-configured environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other environment variables can be provided by the user, via the Control Panel's
*Env Variables* view:

.. image:: /images/env-vars.png
   :alt: 'Adding an environment variable'
   :class: 'main-visual'

If you need the variable in the local development environment, add::

  SECRET_API_KEY = "aaPfaH1oJ5pdqYBc"

to the ``.env-local``.


Manually in ``settings.py``
---------------------------

As mentioned above, all these settings will be applied to the settings file by the
``aldryn_addons.settings.load(locals())`` function. If any of them were written into the file manually *before* this
point, it will overwrite them. Any settings you wish to provide manually should be added *after* the function to avoid
this.


Overwriting automatically-configured settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Overwriting automatically-configured settings is almost always a bad idea.* For example, multiple addons may have
added their own requirements to the ``MIDDLEWARE`` setting. If you simply do::

  MIDDLEWARE = [
     ...
  ]

you will obliterate the automatic configuration (or if you place your setting before
``aldryn_addons.settings.load(locals())``, your own setting will be overwritten). If you need to add middleware, the
safer and more sophisticated way to do it is by **manipulating** the list (see :ref:`how-to-settings`).

To understand which settings are provided automatically, you can:

* examine the addon's ``aldryn_config.py`` file
* check the :ref:`reference documentation for Aldryn Django, Aldryn SSO and Adryn Addons, where many important settings
  are listed <key-addons>`

You can :ref:`list changed settings <list>` to see those that have been altered from Django's own defaults.


.. _envar_setting_field:

In your own addon applications
------------------------------

When writing your own addons, you can choose to provide configuration via any method you like.

Some rules of thumb for the appropriate method:

* For highly-sensitive configuration, such as passwords, use an environment
  variable - it's safer, because it's not stored in the codebase.
* For configuration that is specific to each instance of the codebase, or that
  needs to be different across *Local*, *Test* and *Live* environments,
  environment variables are recommended.
* For required configuration, it is a good idea to make it visible as a field,
  so it's obvious to the user that it needs to be set; similarly if it's
  something that a non-technical user might be expected to set.
* If you provide an addon configuration field, make sure it isn't overridden by
  other configuration, as that could be confusing to the user.
* The ``settings.py`` file makes sense for configuration that isn't sensitive,
  and will be the same in different instances of the codebase and can be the
  same across the different environments.
* The cleaner you keep your ``settings.py``, the better.
