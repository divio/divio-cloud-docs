Set up your project locally
========================================

In this section we will set up locally the cloud project you created earlier.

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

The Divio CLI will execute a number of steps - this make take a few minutes, depending on how much needs to be
downloaded and processed. The Divio CLI tool will build your project locally (see :ref:`build-process` for a
more detailed description of what's happening here):

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


``cd`` into the newly-created project directory, where you will find your project code.
