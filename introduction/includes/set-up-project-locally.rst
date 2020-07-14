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

..  note::

    You can find other useful commands listed in `our local commands cheat sheet
    <https://docs.divio.com/en/latest/reference/local-commands-cheatsheet.html>`_.

The Divio CLI tool will build your project locally. See :ref:`build-process`
for a description of what it does.

``cd`` into the newly-created project directory, where you will find your project code.
