:orphan:

Unpinned Python dependencies
=============================================

**Support notice 16th November 2020**

..  important::

    Unpinned dependency errors are not related to Divio infrastructure or services, and are wholly the responsibility
    of the user to address and prevent.

    Divio Support is not able to provide assistance in the resolution of problems related to unpinned Python
    dependencies.


What is an unpinned dependency?
========================================

An unpinned dependency is any Python component installed in an application whose version is not exactly specified, for
example::

    django

rather than::

    django==3.0.0

It is crucial to understand that even *pinned dependencies may themselves have unpinned dependencies*.

pip will attempt to install the latest version of any dependency it finds. In the case of an unpinned dependency, this
could be a newly-updated and incompatible version of the component. This can cause unexpected build, deployment or
runtime errors.


Pinning Python dependencies
---------------------------

All Python dependencies should be fully pinned once you have a working combination of components.

To obtain a full list, use::

    pip freeze

in the application (either locally, using ``docker-compose run web pip freeze``, or in a 
:ref:`cloud shell <cloud-shell>`.)

The full list should be included in your application's Python requirements file.

If you are using Aldryn Django in your application, see :ref:`manage-dependencies`.

..  note:

    In cloud deployments, Docker layers are not cached, and pip will always find the latest version of a component.
    Locally, Docker Compose caches layers when building an image, and this means that pip will not always include the
    latest version. Therefore problems with unpinned dependencies may become apparent in cloud environments but not
    locally. Use the ``--no-cache`` option with ``docker-compose build`` to ensure that your local application builds
    using the same Python dependencies as on the cloud.
