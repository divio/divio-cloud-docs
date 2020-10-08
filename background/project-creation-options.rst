.. _project-creation-options:

Project creation options
==============================

Each Divio project is based on a combination of *Stack*, *Additional components* and *Additional Boilerplate*.

Any application that is suited to being run in Docker can be run on Divio and build up using the default *Build your
own* option as a starting point.

We also provide some optional ready-to-go definitions for a quick start. For example:

* **Stack**: *Aldryn Python*
* **Additional components**: *django CMS*
* **Additional Boilerplate**: *HTML5*

It's important to understand that these pre-built project templates are simply there to provide you with a quick way to
get started with a particular stack. They don't prevent you from adding other components; for example, you might decide
to :ref:`add Sass CSS compilation using Node to a project that doesn't already include Node <configure-sass>`.


..  Do not change this reference!
    Referred to by: tutorial message 51 project-create-base-project
    Where: in the project creation dialog e.g. https://control.divio.com/control/project/create/#step-1
    As: https://docs.divio.com/en/latest/background/project-creation-options#project-creation-platform

.. _project-creation-platform:

Stack
---------

Options include Build your own, Aldryn Python, Node, PHP, Java and others.

:ref:`django-create-deploy` for a good example of using the *Build your own* option with Django.


..  Do not change this reference!
    Referred to by: tutorial message 52 project-create-type
    Where: in the project creation dialog e.g. https://control.divio.com/control/project/create/#step-1
    As: https://docs.divio.com/en/latest/background/project-creation-options#project-creation-type

.. _project-creation-type:

Additional components
----------------------

The available additional components depend on the selected Stack.

For the Aldryn Python platform, examples include Django, django CMS and Flask; for the PHP platform, Laravel and
Symfony, and so on.


..  Do not change this reference!
    Referred to by: tutorial message 53 project-create-boilerplate
    Where: in the project creation dialog e.g. https://control.divio.com/control/project/create/#step-1
    As: https://docs.divio.com/en/latest/background/project-creation-options#project-creation-boilerplate

.. _project-creation-boilerplate:

Additional Boilerplate
-----------------------

Available Boilerplates depend on the additional components selected.

Boilerplates provide additional functionality baked into the project. For example, an Aldryn Python/django CMS project
can be launched with Boilerplates for Bootstrap, Foundation and other technologies.


..  Do not change this reference!
    Referred to by: tutorial message 116 project-creation-repo-intro
    Where: in the project creation dialog e.g. https://control.divio.com/control/project/create/#step-1
    As: https://docs.divio.com/en/latest/background/project-creation-options#project-creation-repository-manager

.. _project-creation-repository-manager:

Git repository manager
----------------------

By default, your project will use Divio's own private Git server. Alternatively you can select a Git provider of your
choice. You can :ref:`migrate a project from our Git server to an external provider at any time
<configure-version-control>`.

For a quick start, use Divio's Git server.
