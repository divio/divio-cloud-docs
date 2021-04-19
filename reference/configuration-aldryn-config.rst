..  This section is referred to (as http://docs.divio.com/en/latest/reference/configuration-aldryn-config.html) from
    within the settings.py file provided by standard Aldryn Django projects. Do not change this reference.

.. _configure-with-aldryn-config:

Addon configuration with ``aldryn_config.py``
===================================================

..  note:: Aldryn continues to be supported by Divio, but we do not recommend using Aldryn Django for new applications.

A Django application may require some configuration when it is deployed in a
project. Typically this will include settings in :ref:`settings.py
<settings.py>`, but it can also include things like URL patterns that need to
be set up.

For Aldryn addons, Divio provides for such configuration through an addon's
``aldryn_config.py`` file. This file needs to be in the root directory of the
addon.

Through this mechanism you can also allow the user to provide configuration in
a simple web form that will be available in the Control Panel.

When the user saves the web form, the data will be stored in the addon's ``settings.json`` file in
the project repository.

An example from a django CMS addon instance::

    {
        "boilerplate_name": "html5",
        "cms_content_cache_duration": 60,
        "cms_menus_cache_duration": 3600,
        "cms_templates": "[[\"content.html\", \"Content\"], [\"sales.html\", \"Sales\"]]",
        "permissions_enabled": true
    }


.. _aldryn-config-how-to:

The ``aldryn_config.py`` file
-----------------------------

This file contain a class named ``Form`` that sub-classes
``aldryn_client.forms.BaseForm``::

    from aldryn_client import forms


    class Form(forms.BaseForm):
        ...

The Form class will contain the logic required to manage configuration.


Managing settings
-----------------

A ``to_settings()`` method on the ``Form`` class will be called. Use this to
return a dictionary of settings.

It takes two arguments:

* the ``cleaned_data`` from the form
* a dictionary containing the existing settings

Add or manipulate the settings in the dictionary as required, and return it.

If you wish to accept user-supplied configuration, you will need to add some
form fields to the form (see :ref:`adding-form-fields` below).


.. _how-to-manage-url-configuration:

Managing URL configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

``ADDON_URLS`` (and :ref:`related settings <addon-urls>`) to help manage URL
configurations via settings.

We can define them in the ``to_settings()`` method of an application to do this.

Here’s an example of ``aldryn_config.py`` that inserts URL configurations into
a project:

..  code-block:: python
    :emphasize-lines: 6

    from aldryn_client import forms

    class Form(forms.BaseForm):
        def to_settings(self, data, settings):

            settings['ADDON_URLS'] = 'django_example_utilities.urls'

            return settings


See :ref:`addon URLs <addon-urls>` for details.


.. _adding-form-fields:

Adding form fields for user-configuration of the Addon
------------------------------------------------------

The ``Form`` class may contain any number of form fields.

Available fields are:

* ``aldryn_client.forms.CharField`` (optional arguments: ``min_length`` and
  ``max_length`` )
* ``aldryn_client.forms.CheckboxField``
* ``aldryn_client.forms.SelectField`` (required second argument: a list of
  tuples)
* ``aldryn_client.forms.NumberField`` (optional arguments: ``min_value`` and
  ``max_value`` )
* ``aldryn_client.forms.StaticFileField`` (optional argument: ``extensions`` ,
  a list of valid file extensions.)

All fields must provide a label as first argument and take a keyword argument
named ``required`` to indicate whether this field is required or not.

Here's an example:

..  code-block:: python

    class Form(forms.BaseForm):
        # get the company name
        company_name = aldryn_client.forms.CharField("Company name", required=True)

        def to_settings(self, cleaned_data, settings_dict):
            # set the COMPANY_NAME based on company_name
            settings_dict['COMPANY_NAME'] = cleaned_data[company_name"]

            # if we are in DEBUG mode, as on the Test server, use the Django console backend
            # rather than really sending out messages (see
            # https://docs.djangoproject.com/en/1.8/topics/email/#console-backend)
            if settings_dict.get('DEBUG'):
                settings_dict['EMAIL_BACKEND'] = 'django.core.mail.backends.console.EmailBackend'

            return settings_dict


Custom field validation
-----------------------

For custom field validation, sub-class a field and overwrite its ``clean()`` method. The ``clean()`` method takes a single argument (the value to be cleaned) and should either return a cleaned value or raise a ``aldryn_client
.forms.ValidationError`` with a useful message about why the validation failed.

Example::

    from aldryn_client import forms


    class FavouriteColourField(CharField):
        def clean(self, colour):
            colour = super(FavouriteColourField, self).clean(colour)
            if colour == "black":
                raise forms.ValidationError("You can have any colour you like except black")
            else:
                return colour


.. _envar_setting_field:

What configuration method to provide?
-------------------------------------

There are multiple ways of providing configuration in the addons you create - see :ref:`application-configuration` for
an overview. You can choose to provide configuration via any method you like, but some rules of thumb for the
appropriate method:

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

