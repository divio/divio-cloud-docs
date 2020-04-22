.. _application-configuration:

How settings are handled in Django addons
=========================================

In Django projects, settings are handled via the :doc:`settings <django:topics/settings>` module (usually, the ``settings.py`` file).

In projects that use Aldryn Django, settings can be applied in multiple ways.

Most key settings of Aldryn addons (addons that include an ``aldryn_config.py`` file) are managed via the addon itself, and then
applied to the settings module via the lines::

  import aldryn_addons.settings
  aldryn_addons.settings.load(locals())

From this point in the file, the settings that were automatically configured by the addon will be available in the ``settings.py`` file.
For example, the project's ``addons/aldryn-django/aldryn_config.py`` will add entries to ``INSTALLED_APPS``, ``MIDDLEWARE`` and so on. Such
settings can be determined in a number of ways:


Via Addon settings in the Control Panel
---------------------------------------

An Addon can expose options for configuration in the Control Panel interface. For example, Aldryn Django has a
:ref:`PREFIX_DEFAULT_LANGUAGE` option. This will apply to all cloud environments of the project. For the local development environment, it
will be placed in the project's ``addons/aldryn-django/settings.json``.


By environment variables
------------------------

Environment variables are suitable for:

* secret settings that you don't wish to commit to code
* environment-specific settings

Suppose your Django application requires a secret key ``SECRET_API_KEY`` that allows it to connect to a third-party service. You could
simply add this to the ``settings.py``::

  SECRET_API_KEY = "aaPfaH1oJ5pdqYBc"

This is not ideal from the point of view of security, as the key will now be part of the code-base. It is better to use the Control Panel's
*Env Variables* view to add it:

.. image:: /images/env-vars.png
   :alt: 'Adding an environment variable'
   :class: 'main-visual'




Programatically


Manually in ``settings.py``
---------------------------




Django applications may require or offer configuration options. Typically this
will be achieved via the ``settings.py`` file, or through environment variables
that Django picks up.

This is largely handled by the :ref:`aldryn_config.py
<configure-with-aldryn-config>` in each application.

Divio project offers both these methods, as well as configuration via
the Control Panel:

* Django settings
* :ref:`environment variables <environment-variables>`
* :ref:`addon configuration field <configure-with-aldryn-config>`


.. _envar_setting_field:

Environment variable, setting or Addon configuration field?
-----------------------------------------------------------

When should you adopt each of these methods in your applications?

Rules of thumb:

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
