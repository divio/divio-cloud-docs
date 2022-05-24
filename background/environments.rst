..  Do not change this document name
    Referred to by: tutorial message 151 project-environments-info
    Where: in the Environments view
    As: https://docs.divio.com/en/latest/background/environments

.. _environments:

Environments
============

Each Divio application can have multiple application environments. All applications include a *Test* and *Live* 
environment by default. Each environment of an application is completely distinct and independent, and has its own 
environment variables, containers, database, media storage and other services. All environments in an application use 
the same Git repository, but each can use a different Git branch.

.. image:: /images/environments.png
   :alt: 'Environments'
   :class: 'main-visual'

--------

The view provides options for configuring environments (for example, setting Git branches) as well as access to useful
commands for development, controls for deployment and other actions, and links to deployment and runtime logs.


The *Live* environment
----------------------

The *Live* environment, unlike the other environments:

* never sleeps (the others will shut down their containers after an idle period, to save resources)
* can use multiple containers if specified in the application subscription (the others use only one container)
* can be wired up to the user's own domains


Adding and removing environments (Beta)
---------------------------------------

..  note::

    Functionality to add and remove environments is currently provided as a Beta feature, and is available only to
    users who have signed up for access to Beta-release features. `Enable Beta features in your account settings
    <https://control.divio.com/account/contact/>`_.

The **Add environment** button allows you to create additional environments. For example, you might create a *QA*
environment for in-depth testing of new functionality, or to explore development of functionality in a new branch of
the codebase before it's merged back into the main branch.

Each new environment can be based on an existing environment, or can be set up from scratch.
