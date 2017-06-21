.. _project-anatomy:

Anatomy of a Divio Cloud project
================================

.. _build-process:

The project build process
-------------------------

Local builds
^^^^^^^^^^^^

#.  The Divio CLI clones (downloads) the project's files from the Divio Cloud
    Git server.
#.  The project's ``docker-compose.yml`` file is invoked, telling Docker
    what containers need to be created, starting with the ``web`` container,
    which is built using...
#.  ...the project's ``Dockerfile``. This tells Docker how to build the
    the project's containers - Docker begins executing the commands contained
    in the file.
#.  If necessary, Docker downloads the layers from which the container image
    is built.
#.  Docker continues executing the commands, which will include copying files,
    installing packages using Pip, and running Django management commands.
#.  Docker returns to the ``docker-compose.yml``, which sets up filesystem,
    port and database access for the container, and the database container
    itself.
#.  The ``docker-compose.yml`` file contains a default ``command`` that starts
    up the Django server.
#.  The Divio CLI opens a web browser window with a login page for the locally
    running site.


.. _addon-templates:

Addons' templates in projects
-----------------------------

In your Divio Cloud project directories, you will find a ``templates``
directory. This is the place for your project's templates, such as its own base
templates.

It's also where you can place templates to override addon applications'
templates. Templates at the project level will override templates at the
application level if they are on similar paths. This standard Django behaviour,
allowing application developers to provide templates that can easily be
customised.

For your convenience, when you first create a project, any templates in addons
are copied to the project level so you have them right at hand.

For example, templates from Aldryn News & Blog will be copied to
``templates/aldryn_newsblog/`` in your project.

If a template does not exist in the project's ``templates`` directory, Django
will simply fall back to the one in the addon itself.


Subsequent addon updates
^^^^^^^^^^^^^^^^^^^^^^^^

After templates have been copied to the project's ``templates`` directory, they
will not be copied again, so as not to overwrite any changes the project
developer may have made. However, this does mean that if an addon is
subsequently updated and its templates change, those changes will not appear in
your project.

In this case:

* if you have made changes to the templates in your project, you will need to
  obtain any updated templates and merge them with your own versions
* if you have not made any changes, you can simply delete your local versions
  and Django will use the updated application templates.
