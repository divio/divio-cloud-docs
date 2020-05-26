.. _tutorial-package-addon-cloud:

Package an addon (deployment)
===================================

..  admonition:: This tutorial assumes your project uses Django 1.11

    At the time of writing, version 1.11 is `Django's Long-Term Support release
    <https://www.djangoproject.com/download/#supported-versions>`_, and is
    guaranteed support until at least April 2020.
    
    If you use a different version, you will need to modify some of the code
    examples and version numbers of packages mentioned.


Our Django Debug Toolbar Addon can now install and configure itself in a local
project; next is to complete the work of packaging it so that it can do the
same in a Divio project online.

As noted previously, when addons are installed into projects from the Control
Panel, they can expose their settings to the user via a web form in the
``aldryn_config.py`` file.


Add a field to the configuration form
-------------------------------------

We'll add a checkbox field, to control whether the user wants the Debug Toolbar
to be active or not. The value of the new ``enable_debug_toolbar`` field will
be passed to the ``to_settings()`` method, in the ``data`` dictionary. Then
we'll also test for ``data['enable_debug_toolbar']`` before enabling the
Toolbar:

..  code-block:: python
    :emphasize-lines: 3-7, 13

    class Form(forms.BaseForm):

        enable_debug_toolbar = forms.CheckboxField(
            'Enable Django Debug Toolbar',
            required=False,
            initial=True,
        )

        [...]

        def to_settings(self, data, settings):

            if settings["DEBUG"] and data['enable_debug_toolbar']:

                [...]


We can't actually test this locally - we'll have to upload it before we can do
that.


Add the remaining packaging files
---------------------------------

``LICENSE``
^^^^^^^^^^^

The addon needs a ``LICENSE``, so download that from the Control Panel and move
it to the package.


``MANIFEST.in``
^^^^^^^^^^^^^^^

Do the same for the ``MANIFEST.in``. The default ``MANIFEST.in`` lists the
licence file as well as other directories that an addon is likely to have,
though we don't use any of those in this addon.


``addon.json``
^^^^^^^^^^^^^^

The final packaging file is specific to the Divio, ``addon.json``, which
provides some additional metadata::

    {
        "package-name": "tutorial-django-debug-toolbar",
        "installed-apps": [
            "tutorial_django_debug_toolbar"
        ]
    }

Download it and add it to the addon.


Validate and upload the addon
-----------------------------

Make sure you're in the ``addons-dev/tutorial-django-debug-toolbar`` directory.

Now, running ``divio addon validate`` should now confirm that the addon is
valid::

    ➜ divio addon validate
    Addon is valid!

and it's ready to be uploaded with ``divio addon upload``::

    ➜  divio addon upload
    warning: no files found matching '*' under directory '*/boilerplates'
    warning: no files found matching '*' under directory '*/templates'
    warning: no files found matching '*' under directory '*/static'
    warning: no files found matching '*' under directory '*/locale'
    warning: check: missing required meta-data: url

    ok
    Configuration file is valid


    New version 1.8.0.1 of tutorial-django-debug-toolbar uploaded to alpha channel

    Configure your addon here https://control.divio.com/account/my-addons/878/

Don't worry about the warnings - as long as there are no errors, all is in
order.

As the output notes, this version of the addon has been placed into the *Alpha*
release channel. If you visit its *Versions* page, you'll be able to change
the release channel.


Install the addon in a Cloud project
------------------------------------

If you now visit your project (or any project you have access to) in the
Control Panel, and select its *Addons* menu, you'll be able to select, install
and configure your new addon, complete with the checkbox field you created
earlier.

.. image:: /images/install-toolbar.png
   :alt: 'Divio app'
   :width: 720


If you deploy your Stage server, you'll have the Debug Toolbar running in the
cloud project.


Manage the addon via the Control Panel
--------------------------------------

You can manage your addon, moving particular versions of it into the *Beta* or
*Stable* channels, make it public and so on.

If you make it public, then other users will be able to use it in their projects
too.
