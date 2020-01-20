.. _create-addon:

How to package a Django application as an addon
===============================================

..  seealso::

    * :ref:`Add new applications to the project <tutorial-add-applications>` tutorial
    * If you simply want to add an application to a project and don't need to
      package it as an addon, see :ref:`add-application` instead.


Register the addon
------------------

Before your addon can be uploaded, the Divio Cloud must be ready to receive it.

Select **Add custom addon** from `Personal Addons in the Divio Control Panel
<https://control.divio.com/account/my-addons/>`_, or simply go straight to `Add custom addon
<https://control.divio.com/account/my-addons/new/>`_.

* *Package Name*: must be unique on the system. We recommend prefixing it with your own name, for
  example ``susan-example-application``.
* *Name*: e.g. ``Susan's Django Debug Toolbar``
* *License*: select a predefined license for your addon (or leave it blank and add your own later.)
* *Organisation*: select an organisation if appropriate.

When you hit **Create addon**, the addon will be registered on the system.

..  important::

    The package name **must not** contain underscores. See the note in :ref:`the addon packaging
    tutorial <tutorial-package-addon>` for more information.


Add the packaging files
-----------------------

We need to work in the project's ``addons-dev`` directory. Create a new
directory there with the same name as the *Package Name*.

Select *Package Information* from your addon's menu. Download the packaging
files, and add them to the addon. It should look something like this::

    addons-dev/
        susan-example-application/
            addon.json
            LICENSE
            MANIFEST.in
            README.rst
            setup.py
            susan_example_application/
                __init__.py

Now let's go through the files one by one.


The ``setup.py`` file
^^^^^^^^^^^^^^^^^^^^^

All the lines you need in the :ref:`setup-py` will be provided automatically in
the downloaded version, with the exception of the ``install_requires``
argument:


If your addon *installs* an application
.......................................

In this case, you will need to add the package to be installed to the
``install_requires`` argument, for example
``install_requires=["example_application==1.8.3"]``.


If your addon *contains* an application
.......................................

On the other hand, if for example, the application is not available on PyPI,
simply add it as the inner application directory.

.. _addon_application_naming:

..  important::

    The *inner application directory*, in this case ``susan_example_application``, should have a
    name that matches the *package name* (``susan-example-application``), with underscores
    substituting for the dashes.

    This will allow the Control Panel to copy the application's templates into the project's
    Git repository when the addon is first installed in a project. If the names don't match,
    the project will still work, but the templates will not be made available for easy editing.


The addon will then contain some additional files:

..  code-block:: text
    :emphasize-lines: 6-12

    addons-dev/
        susan-example-application/
            [...]
            susan_example_application/
                __init__.py
                admin.py
                apps.py
                migrations/
                    __init__.py
                models.py
                tests.py
                views.py

Add any dependencies of the application to ``install_requires`` of ``setup.py``.


The ``__init__.py`` file
^^^^^^^^^^^^^^^^^^^^^^^^

``setup.py`` expects to find a version number in the addon, at
``tutorial_django_debug_toolbar.__version__``:


For an addon that *installs* a package
.......................................

We recommend providing a version number that *tracks* the package's version
number - for example, if the addon installs version ``1.8.3``, the addon's
``__version__`` numbers should be ``1.8.3.1``, ``1.8.3.2`` and so on.


For an addon that *includes* a package
.......................................

We recommend some form of semantic versioning.


The other packaging files
^^^^^^^^^^^^^^^^^^^^^^^^^

The other packaging files are simpler:

* ``README.rst``: If you haven't already provided a description via the Control Panel, this will be
  empty. If you plan to share your addon with other users, it's important to provide a useful
  README.
* ``MANIFEST.in``: The default ``MANIFEST.in`` takes care of most non-Python files that an addon is
  likely to need the setup tools to take care of: ``LICENSE``, plus directories for LICENSE, plus
  directories for ``boilerplates``, ``templates``, ``static`` and ``locale`` files.
* ``LICENSE``: Make sure the license terms are appropriate.
* ``addon.json``: We recommend leaving this as it is. Although you can use it to add multiple
  packages to ``INSTALLED_APPS``, it's better to do this in ``aldryn_config.py`` (see below).


Add configuration
-----------------

.. _create-aldryn-config:

Create ``aldryn_config.py``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your application requires any settings of its own, you will need to manage
them in ``aldryn_config.py``, placed at the root of your application. The general form is:

..  code-block:: python
    :emphasize-lines: 6,7

    from aldryn_client import forms

    class Form(forms.BaseForm):
        def to_settings(self, data, settings):

            settings['INSTALLED_APPS'].extend([SOME_APPLICATION])
            settings['ENABLE_FLIDGETS'] = True

            return settings

See :ref:`how to configure settings in
aldryn_config.py <aldryn-config-how-to>` for more details and examples.


Provide form-based configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use the ``Form`` class to allow configuration via the Control Panel.

See :ref:`adding form fields for user configuraion <adding-form-fields>`
for more information.


Provide URL configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

Not all addons will have their own URL configurations that need to be included
in a project, but if they do, you can add them. See :ref:`how to include an addon's URL configuration <how-to-manage-url-configuration>` for more details.


Check the addon
---------------

Test it
^^^^^^^

Your addon is now ready to be tested.

Add the package name to the ``INSTALLED_ADDONS`` in ``settings.py``. This
adds it to the list of addons that the project will “watch”.

Run::

    divio project develop <package name>

You can test that the project now works as expected.


Validate it
^^^^^^^^^^^

Now make sure you're in the ``addons-dev/<package name>`` directory.

Now, running ``divio addon validate`` should now confirm that the addon is
valid::

    ➜ divio addon validate
    Addon is valid!


Upload the addon
----------------

Upload with ``divio addon upload``.

This version of the addon will be placed into the *Alpha* release channel. If
you visit its *Versions* page, you'll be able to change the release channel.

Your addon is now available for installation into projects via the control
panel. If you make it public, other users will be able to install it too.

You can continue uploading new versions of it, as long as each has its own
unique version number.
