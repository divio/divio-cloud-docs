.. _application-configuration:

Working with Django addons (legacy)
=========================================

..  note:: Aldryn continues to be supported by `Divio <https://www.divio.com>`_, but we do not recommend using Aldryn 
  Django for new applications.

In Django applications, settings are handled via the :doc:`settings <django:topics/settings>` module (usually, the
``settings.py`` file).

In Aldryn addons - those that include an ``aldryn_config.py`` file - many of these settings will be automatically
managed by the addon itself. This takes place in ``aldryn_config.py``.

All key settings (i.e. settings required for the package to function correctly) as well as many optional settings will
be configured. They are then applied to the settings module via the lines::

 import aldryn_addons.settings
 aldryn_addons.settings.load(locals())

From this point in the settings module, those settings that were automatically configured by the addon will be available
in the ``settings.py`` file.

For example, in a Django application, you will find a file::

  addons/aldryn-django/aldryn_config.py

This files adds items to the ``INSTALLED_APPS``, ``MIDDLEWARE``, and applies other settings.

These settings can be controlled and determined in a number of different ways.


Via addon settings in the Control Panel
---------------------------------------

An addon can expose options for configuration in the Control Panel interface. For example, Aldryn Django has a
:ref:`PREFIX_DEFAULT_LANGUAGE` option. This will apply to all environments of the application.

The value is stored in JSON. You can find the JSON file in the application locally, for example
``addons/aldryn-django/settings.json``.


.. _application-configuration-env-vars:

Via environment variables
--------------------------

Environment variables are suitable for:

* environment-specific settings (e.g. database settings, since each environment should have its own)
* secret settings (e.g. keys for services and APIs)

*Environment variables are better than the codebase for such settings.* If committed as part of the codebase, they
provide the same value in all environments, and they are vulnerable to being accidentally shared.


Via automatically applied environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some environment variables are provided automatically, and you don't need to do anything about them at all.

Each application environment has its own variables provided for services such as the database 
(:ref:`DEFAULT_DATABASE_DSN <env-var-database-dsn>`), media storage (:ref:`DEFAULT_STORAGE_DSN <env-var-storage-dsn>`) 
and so on. Locally, the variables are saved in the ``.env-local`` file and 
:ref:`loaded into the environment via docker compose <docker-compose-env>`.


Via user-configured environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other environment variables can be provided by the user, via the Control Panel's *Env Variables* view:

.. image:: /images/env-vars.png
   :alt: 'Adding an environment variable'
   :class: 'main-visual'

If you need the variable in the local development environment as well, add (for example)::

  SECRET_API_KEY = "aaPfaH1oJ5pdqYBc"

to its ``.env-local``.


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
``aldryn_addons.settings.load(locals())``, your own setting will be overwritten).

If for example you need to specify additional middleware, the safer and more sophisticated way to do it is by
**manipulating** the list (see :ref:`how-to-settings`).

To understand which settings are provided automatically, you can:

* examine the addon's ``aldryn_config.py`` file
* check the :ref:`reference documentation for Aldryn Django, Aldryn SSO and Adryn Addons, where many important settings
  are listed <key-addons>`

You can :ref:`list changed settings <list>` to see those that have been altered from Django's own defaults.



.. _addon-anatomy:

Anatomy of a Divio addon
---------------------------

..  note:: Aldryn continues to be supported by `Divio <https://www.divio.com>`_, but we do not recommend using Aldryn 
  Django for new applications.


Basic file structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For an addon "Susan Example Application"::

    addons-dev/
        susan-example-application/
            addon.json
            LICENSE
            MANIFEST.in
            README.rst
            setup.py
            susan_example_application/
                __init__.py



.. _aldryn-config:

``aldryn_config.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All addons have an ``aldryn_config.py`` file that takes care of settings, which are then loaded into 
:ref:`settings.py <settings.py>`.

This means that any settings you need to apply in an application can't simply be applied in your ``settings.py`` if an 
addon also needs access to them.

For example, nearly every addon will add a package, or sometimes several, to ``INSTALLED_APPS``. If you were to assign 
do ``INSTALLED_APPS = [...]`` in the usual way, you would overwrite the existing assignments and break the application.
That's why our ``settings.py`` uses::

    INSTALLED_APPS.extend([
        # add your application specific apps here
    ])

The same goes for middleware, and other settings.

``aldryn_config.py`` is loaded into the Django application at runtime, so any changes are picked up when and reloaded 
automatically when developing.

``aldryn_config.py`` is an ideal place to check for environment variables that should be converted into Django settings.

See :ref:`configure-with-aldryn-config`.


``addon.json``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A metadata file.

::

    {
        "package-name": "susan-example-application",
        "installed-apps": [
            "susan_example_application"
        ]
    }


.. _setup-py:

``setup.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``setup.py`` will be generated by the Control Panel on the basis of the information you provided when you first created 
it there. The lines highlighted below are those that will be specific to your addon:

..  code-block:: python
    :emphasize-lines: 2, 7, 10, 11, 14

    # -*- coding: utf-8 -*-
    from setuptools import setup, find_packages
    from susan_example_application import __version__


    setup(
        name='susan-example-application',
        version=__version__,
        description=open('README.rst').read(),
        author='Susan',
        author_email='susan@example.com',
        packages=find_packages(),
        platforms=['OS Independent'],
        install_requires=["example_application==1.8.3"],
        include_package_data=True,
        zip_safe=False,
    )


.. _addon-templates:

Django addons and templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Templates at the application level will override templates at the application level if they are on similar paths. This 
is standard Django behaviour, allowing application developers to provide templates that can easily be customised.


On initial application creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For your convenience, when you first create an application, any templates in addons are copied to the application level 
so you have them right at hand (*if* the addon's 
:ref:`package name and inner application name match <addon_application_naming>`.)

For example, templates from Aldryn News & Blog will be copied to ``templates/aldryn_newsblog/`` in your application.

If a template does not exist in the application's ``templates`` directory, Django will simply fall back to the one in 
the addon itself.


Subsequent addon updates
^^^^^^^^^^^^^^^^^^^^^^^^^^

After templates have been copied to the application's ``templates`` directory, they will not be copied again, so as not 
to overwrite any changes the application developer may have made. However, this does mean that if an addon is 
subsequently updated and its templates change, those changes will not appear in your application.

In this case:

* if you have made changes to the templates in your application, you will need to obtain any updated templates and 
  merge them with your own versions
* if you have not made any changes, you can simply delete your local versions and Django will use the updated 
  application templates.
