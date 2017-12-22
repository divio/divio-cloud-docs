.. _update-addon:

How to update an existing addon
===============================

Addons will need to be updated now and then. The basic process for updating an addon is to:

* :ref:`set it up in a project as if you were creating one <create-addon>`, in the ``addons-dev``
  directory
* make and test your changes
* upload the new version.


Set up a local project
----------------------

It's recommended to work with a project that already contains the addon. This way, you can check
that the new version continues to work as expected, and that migrations for example run correctly.

If you don't, the next best way is to create a new project on the Control Panel containing the
addon, and then set that up locally.

Get the project running locally, for example with ``docker-compose up``. If you're updating the
addon because it no longer works correctly (a common issue is that an unpinned dependency installs
an incompatible component) then this won't be possible.


Uninstall the addon locally if necessary
----------------------------------------

You will find the addon:

*  as a directory in the ``addons`` directory
* listed in ``requirements.in``.

Remove it from each of these places.

You will also find it listed in ``INSTALLED_ADDONS`` in ``settings.py`` - *leave it there*.


Clone the addon repository to ``addons-dev``
--------------------------------------------

It should look something like this::

    addons-dev/
        susan-example-application/
            addon.json
            LICENSE
            MANIFEST.in
            README.rst
            setup.py
            susan_example_application/
                __init__.py

Make sure you checkout the **same** version of it as was previously installed.


Check that it behaves as before
-------------------------------

Restart the runserver (``docker-compose up``), and check that the addon continues to work as
expected (or fails to work, if that is what previously happened).


Make and test your changes
--------------------------

Make your updates to the addon, checking that they work as expected.

Run::

    divio project develop <package name>

This processes the addon, adding::

    -e /app/addons-dev/<package name>

to the ``requirements.in``.

You will need to run this if you make any changes in the addon that involve dependencies or
installation of components.


Push your changes
-----------------

You'll need to bump the version number in the ``__init__.py``.

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
