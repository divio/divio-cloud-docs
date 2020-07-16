..  This include is used by:

    * django-04-add-application.rst
    * wagtail-04-add-application.rst


A brief explanation of Aldryn Addons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This project uses the optional Aldryn Addons system, which makes it possible for projects to configure themselves. For
example, you can can find all the configuration that Aldryn Django does for Django settings in
``addons/aldryn-django/aldryn_config.py``. (Aldryn Django is simply a convenience wrapper for Django - the Django used
by your project is a wholly standard Django installation obtained from PyPI.)

*You don't have to use Aldryn Addons* on Divio; if you prefer to manage settings manually, that will work just as well.
However it makes development much faster, as it takes care of all the settings that would otherwise need to be managed
correctly for the different cloud environments as well as the local environment.

One advantage of Aldryn Django is that it declutters the ``settings.py file``, removing deployment-related values that
are better handled via environment variables, and also provides a guarantee that settings for database, media and so on
will always be correct. Aldryn Django's ``aldryn_config.py`` sets them appropriately for each environment, including
the local development environment, and also appropriately at each stage of the build/deployment process.

In ``settings.py``, you'll find the lines:

..  code-block:: python

    import aldryn_addons.settings
    aldryn_addons.settings.load(locals())

These lines load all those settings into the ``settings`` module. This includes populating ``INSTALLED_APPS``. A
good way to see what settings are applied is via Django's ``diffsettings`` command:

..  code-block:: bash

   docker-compose run web python manage.py diffsettings

