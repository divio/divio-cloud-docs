..  Do not change this document name!
    Referred to by: Aldryn django CMS repository
    Where: https://github.com/divio/aldryn-django-cms/readme.rst
    As: https://docs.divio.com/en/latest/how-to/addon-update-existing


.. _update-addon:

How to update an existing addon
===============================

Addons will need to be updated now and then. The basic process for updating an addon is to:

* :ref:`set it up in a project as if you were creating one <create-addon>`, in the ``addons-dev``
  directory
* make and test your changes
* upload the new version.


Choose a local project to work with
-----------------------------------

Ideally, select a project that already works with an existing version of the addon. This way, you can check
that the new version continues to work as expected, and that migrations for example run correctly.

If you don't have such a project, the next best thing is to create a new project on the Control Panel
containing the addon, and then set that up locally.


Uninstall the addon locally if necessary
----------------------------------------

You will find the addon listed in ``requirements.in`` - remove it from there, so that when you build the
local container it will no longer try to install the old version.

You will also find it listed in ``INSTALLED_ADDONS`` in ``settings.py`` - *leave it there*.


Clone the addon repository to ``addons-dev``
--------------------------------------------

In ``addons-dev``, clone the addon from its VCS repository. It should look something like this::

    addons-dev/
        susan-example-application/
            addon.json
            LICENSE
            MANIFEST.in
            README.rst
            setup.py
            susan_example_application/
                __init__.py

Check that you have the appropriate version cloned.

Placing the addon into ``addons-dev`` will override any version that has been installed into the project
using the requirements file.


Run ``divio project develop``
-----------------------------

If the new version is different from the previously installed version and includes changed dependencies, or
you want to check exactly what it will do when when the project is built, you should run::

     divio project develop <package name>

This processes the addon, adding::

    -e /app/addons-dev/<package name>

to the ``requirements.in``.

**You will need to run this again** if you make any changes in the addon that involve dependencies or
installation of components.


Work on the code
----------------

Restart the runserver (``docker-compose up``), and check that the addon continues to work as
expected (or fails to work, if that is what previously happened).

Make and test any changes you want to make.


Push your changes
-----------------

When you're satisfied, you're ready to update the addon.

Don't forget to bump the version number in the ``__init__.py``.

When you have finished all your updates, commit and push your changes to the addon's repository (or
make a pull request if it's not your own).

Remember that if your addon is a wrapper for installing a reusable application,
its version number should track the version number of the application, in an additional dotted
increment - for example, the addon version ``1.5.4.2`` tracking application version ``1.5.4``
should become ``1.5.4.3``.


Upload the new addon version
----------------------------

Finally, in the addon directory, run::

    divio addon validate

to check it, and::

    divio addon upload

to push it to the addons system.


Test it on the Control Panel
----------------------------

For completeness, check that the new version of your addon can be installed and deployed in a
project.


Place the new version in the appropriate channel
------------------------------------------------

By default, your newly-uploaded addon version will be placed in the Alpha channel. In the *Addons*
section of the Control Panel, put it in the Beta or Stable channels if appropriate.
