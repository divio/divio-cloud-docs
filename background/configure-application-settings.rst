.. _configure-application-settings:

Application configuration with ``aldryn_config.py``
===================================================

A Django application may require some configuration when it is deployed in a
project. Typically this will include settings in ``settings.py``, but it can
also include things like URL patterns that need to be set up.

Divio Cloud provides for such configuration through an addon's
``aldryn_config.py`` file. This file needs to be in the root directory of the
Addon.

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

See the :ref:`aldryn-config` reference for more detail.

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


