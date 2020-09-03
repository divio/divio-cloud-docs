..  This include is used by:

    * django-03-setup-project-locally.rst
    * aldryn-django-03-setup-project-locally.rst
    * wagtail-03-setup-project-locally.rst
    * laravel-03-setup-project-locally.rst


Set up your project locally
========================================

In this section we will build the new project you've created in the local development environment; that is, we will set
it up on your own computer.

Obtain the project's slug (its unique ID) from the Dashboard:

..  image:: /images/intro-slug.png
    :alt: 'Project slug'
    :width: 483

Alternatively you can use the ``divio`` command to list your cloud project, which will show their slugs:

..  code-block:: bash

    divio project list


Build the project locally
-------------------------

Run the ``divio project setup`` command (for example if your project slug is ``tutorial-project``):

..  code-block:: bash

    divio project setup tutorial-project

The Divio CLI will execute a number of steps - this may take a few minutes, depending on how much needs to be
downloaded and processed. The Divio CLI tool will build your project locally (see :ref:`build-process` for a
more detailed description of what's happening here). Note that depending on the project, you won't necessarily see
all the intermediate steps here:

..  code-block:: text

    Creating workspace

    cloning project repository
    [...]
    downloading remote docker images
    [...]
    building local docker images
    [...]
    creating new database container
    [...]
    syncing and migrating database
    [...]
    Your workspace is setup and ready to start.

As well as cloning the repository and attempting to build the project, the ``setup`` command will add a ``.divio``
directory containing some Divio-related configuration that connects it to the Control Panel.

``cd`` into the newly-created project directory, where you will find your project code.
