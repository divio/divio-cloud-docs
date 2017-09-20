.. _application-configuration:

Application configuration overview
==================================

Django applications may require or offer configuration options. Typically this
will be achieved via the ``settings.py`` file, or through environment variables
that Django picks up.

Divio Cloud projects offers both these methods, as well as configuration via
the Control Panel:


* Django settings
* :ref:`environment variables <environment-variables>`
* :ref:`addon configuration field <configure-application-settings>`


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
