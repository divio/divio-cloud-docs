.. _tutorial-package-addon:

Package an addon (installation)
===============================

..  admonition:: This tutorial assumes your project uses Django 1.11

    At the time of writing, version 1.11 is `Django's Long-Term Support release
    <https://www.djangoproject.com/download/#supported-versions>`_, and is
    guaranteed support until at least April 2020.
    
    If you use a different version, you will need to modify some of the code
    examples and version numbers of packages mentioned.


So far we have added applications by adding a module into the project directory
or installing via pip.

In each case, the applications had to be configured. However, this
configuration can be automated, making it possible to create *self-configuring
applications*, that take care of applying the necessary settings when they are
added to a project - so you can install them without having to touch your
``settings.py`` at all.

This is done by providing an application with an :ref:`aldryn_config.py
<aldryn-config>` file, in which the application will check the project and
ensure that ``INSTALLED_APPS``, ``urls.py`` and other key configuration
settings are correct.

The Divio Cloud also allows applications to be installed into projects from the
Control Panel, selecting the version to be installed and configuring the
application - i.e. applying some settings - using a web form. This is also
handled by the same ``aldryn_config.py`` file.

In this section of the tutorial, we'll start packaging Django Debug Toolbar as
a Divio Cloud addon, so that it can install itself into a project.

..  important::

    In the examples below, pay particular attention to the use of dashes ``-``
    and underscores ``_`` in the names of files and directories.

    In Python naming conventions, a *package* name will use *dashes*, as in
    ``tutorial-django-debug-toolbar``. The *application* name within the package will use
    *underscores*: ``tutorial_django_debug_toolbar``.

    This is significant, because although underscores are theoretically allowed in package names,
    various tools, including ``pip``, will silently convert them to dashes, with predictably
    confusing results.


Register the addon
------------------

Before your addon can be uploaded, the Divio Cloud must be ready to receive it
(just as GitHub requires you to create the repository on the platform before
you can push a local repository)

Go to `your addons in the Divio Control Panel
<https://control.divio.com/account/my-addons/>`_ and **Add custom addon**.

The *Package Name* field is the most important, and must be unique on the
system. Call it ``<your name>-django-debug-toolbar``.

..  important::

    From this point onwards for convenience we will refer to this as
    ``tutorial-django-debug-toolbar`` in examples - but you need to substitute
    ``<your name>-django-debug-toolbar``, that you registered the addon with.

    **Every time you see "tutorial", remember to use your own name instead.**

The other fields:

*Name*
    ``<your name> Django Debug Toolbar``
*License*
    Select a license for your addon
*Organisation*
    You can leave this blank

.. image:: /images/add-custom-addon.png
   :alt: 'Add custom addon'
   :width: 720


When you hit **Create addon**, the addon ``tutorial-django-debug-toolbar`` will
be registered on the system. On the next page, supply a *Description* for the
addon::

    Tutorial Django Debug Toolbar
    =============================

    A Divio Cloud addon to install and configure Django Debug Toolbar into
    Divio Cloud projects. Created as part of the Divio Cloud developer
    tutorial.

and hit **Save** once more.


Add the packaging files
-----------------------

We need to work in the project's ``addons-dev`` directory. Create a new
``tutorial-django-debug-toolbar`` directory in there.

Select *Package Information* from your addon's menu. From here, you'll be able
to download system-created versions of the required packaging files. Of course
you can also create them yourself, but this will save you the trouble.


.. _setup.py_tutorial:

Add ``setup.py``
^^^^^^^^^^^^^^^^

In the current set-up, we install the Django Debug Toolbar package manually. We
still want it to be installed, but we need the addon to take care of the
installation for us instead.

Remove ``django-debug-toolbar==1.8`` from ``requirements.in``.

If you now rebuild the project and try to run it, you'll get an error::

    ➜ docker-compose build web
    Building web
    [...]
    Successfully built 9317b86c7745
    ➜ docker-compose up
    [...]
    web_1  | ImportError: No module named debug_toolbar


Instead, move the ``setup.py`` file you downloaded to
``tutorial-django-debug-toolbar`` to handle installation. You'll need to make one change in it:

..  code-block:: python
    :emphasize-lines: 14

    # -*- coding: utf-8 -*-
    from setuptools import setup, find_packages
    from tutorial_django_debug_toolbar import __version__


    setup(
        name='tutorial-django-debug-toolbar',
        version=__version__,
        description=open('README.rst').read(),
        author='Django Developer',
        author_email='developer@example.com',
        packages=find_packages(),
        platforms=['OS Independent'],
        install_requires=["django-debug-toolbar==1.8"],
        include_package_data=True,
        zip_safe=False,
    )


..  note:

    *You* are the author of this addon, and the licence should be the licence
    under which *you* wish to release your addon.

    Your addon is *not* Django Debug Toolbar itself - that is just a dependency
    of your addon. By all means link to Django Debug Toolbar and mention its
    authors in the


Add ``__init__.py``
^^^^^^^^^^^^^^^^^^^

You'll see from the ``setup.py`` that it expects to find a version number at ``tutorial_django_debug_toolbar.__version__``:

..  code-block:: python
    :emphasize-lines: 6

    from tutorial_django_debug_toolbar import __version__


    setup(
        [...]
        version=__version__,
        [...]
    )

Create a new directory inside the addon, named
``tutorial_django_debug_toolbar``. Download and move the the ``__init__.py``
file provided by the Control Panel to the new directory.

By default it declares the version number as ``0.0.1``, but we recommend
tracking the version number of the application that it installs (in this case,
``1.8``) so change it to::

    __version__ = "1.8.0.1"

(If you create another version of the addon to install
``django-debug-toolbar==1.8``, that would be version ``1.8.0.2``. For version
1.9, you'd start at ``1.9.0.1`` and so on.)


Add ``README.rst``
^^^^^^^^^^^^^^^^^^

The ``setup()`` of ``setup.py`` expects to find a README file:

..  code-block:: python
    :emphasize-lines: 3

    setup(
        [...]
        description=open('README.rst').read(),
        [...]
    )


Download and add the ``README.rst`` file. If you haven't already provided a
*Description* via the Control Panel, it will be empty, otherwise, it will
contain the description.


Build the project with the new addon
------------------------------------

We're now ready to build the project. Check that the addon file structure looks
like this::

    addons-dev/
        tutorial-django-debug-toolbar/
            tutorial_django_debug_toolbar/
                __init__.py
            README.rst
            setup.py

and run::

    divio project develop tutorial-django-debug-toolbar

::

    ➜  divio project develop tutorial-django-debug-toolbar
    Building web
    [...]
    The package tutorial-django-debug-toolbar has been added to your local development project!

See the :ref:`divio project develop reference <divio-project-develop>` for more.

You can test that it works by starting the project again (``docker-compose
up``).

Once ``divio project develop <addon>`` has been run, it doesn't need to be
executed again. From this point henceforth any changes you make to the addon,
other than in its ``setup.py``, can be picked up automatically, even while the
project is still running.

Note that:

* Adding new files may require you to restart the server.
* Changes to ``setup.py`` will require running ``docker-compose build web``.

We now have mechanism for *a self-installing addon package*. The next step
is configuration.
