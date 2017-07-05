.. _create-addon:

How to package a Django application as an addon
===============================================

..  note::

    This article assumes you are already familiar with the steps involved. For
    a full walk-through, see the :ref:`tutorial-add-applications` section of
    the :ref:`developer tutorial <introduction>`.

    If you don't need to package an application as an addon, but simply need to
    add it to a project, see :ref:`add-application` instead.


Register the addon
------------------

Before your addon can be uploaded, the Divio Cloud must be ready to receive it.

Go to `your addons in the Divio Control Panel
<https://control.divio.com/account/my-addons/>`_ and **Add custom addon**.

The *Package Name* field must be unique on the system. We recommend prefixing
it with your own name, for example ``susan-example-application``.

The other fields:

*Name*
    ``<your name> Django Debug Toolbar``
*License*
    Select a predefined license for your addon (or leave it blank and add your
    own later.)
*Organisation*
    Select an organisation if appropriate.

.. image:: /images/add-custom-addon.png
   :alt: 'Add custom addon'
   :width: 720

When you hit **Create addon**, the addon will be registered on the system.


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


Check ``setup.py``
^^^^^^^^^^^^^^^^^^

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

If on the other hand, for example if the application is not available on PyPI,
simply add it as the inner application directory.

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


``__init__.py``
^^^^^^^^^^^^^^^^^^^^^

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


Check ``README.rst``
^^^^^^^^^^^^^^^^^^^^

If you haven't already provided a description via the Control Panel, it will be
empty. If you plan to share your addon with other users, it's important to
provide a useful README.


Check ``MANIFEST.in``
^^^^^^^^^^^^^^^^^^^^^

The default ``MANIFEST.in`` takes care of most non-Python files that an addon
is likely to need the setup tools to take care of: ``LICENSE``, plus
directories for LICENSE, plus directories for ``boilerplates``, ``templates``,
``static`` and ``locale`` files.

Add any others that your addon includes.


Check ``LICENSE``
^^^^^^^^^^^^^^^^^

Make sure the license terms are appropriate.


Check ``addon.json``
^^^^^^^^^^^^^^^^^^^^

We recommend leaving ``addon.json`` as it is. Although you can use it to add
multiple packages to ``INSTALLED_APPS``, it's better to do this in
``aldryn_config.py`` (see the following section).


Add configuration
-----------------

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

Add it the package name to the ``INSTALLED_ADDONS`` in ``settings.py``. This
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
you visit the its *Versions* page, you'll be able to change the release channel.

Your addon is now available for installation into projects via the control
panel. If you make it public, other users will be able to install it too.

You can continue uploading new versions of it, as long as each has its own
unique version number.
