..  Do not change this document name!
    Referred to by: Aldryn django CMS repository
    Where: https://github.com/divio/aldryn-django-cms/readme.rst
    As: https://docs.divio.com/en/latest/background/addon-basics

.. _addons-why:

What are addons, and why use them?
==================================

The :ref:`Divio Django addons framework <aldryn-addons>` allows packages to be installed and configured very easily and
in some cases fully automatically.


What are Divio addons?
----------------------

Addons can be thought of as wrappers for Python packages such as Django or django CMS that allow them to take advantage
of our addons framework. You'll see for example addons such as Aldryn Django (a wrapper/installer for Django) and
Aldryn Django CMS (a wrapper/installer for django CMS).

Addons are provided as a convenience. If you'd like Django in your project, with all its settings configured for our
infrastructure (uWSGI gateway, database, media storage etc), and in such a way that they will work correctly in the
Live, Test and local environments, then Aldryn Django will take care of that for you; if it's installed, all that
configuration and wiring will be done automatically.

In the case of Aldryn Django CMS, it will configure settings such as ``MIDDLEWARE`` and ``TEMPLATES`` automatically.

Packages as installed by Divio addons (such as Django or django CMS) are **completely standard and unmodified**.

Installation and basic configuration of addons is managed via the project's dashboard in the Control Panel. More advanced configuration can be managed via :ref:`settings <how-to-settings>` and :ref:`environment variables <environment-variables>`.


Using addons is optional
-------------------------

Using the Addons framework on Divio is completely optional.

You don't *need* Aldryn Django to install or use Django. Similarly, django CMS can be installed and configured
manually, without using Aldryn Django CMS, if you prefer, and the same goes for others.


Why use addons?
---------------

Software installed without taking advantage of the addons framework won't make use of our convenience layers, and it
will require a developer to install and configure them, whereas software packaged as an addon can be installed and
configured with a few clicks, without any technical knowledge.

Using our addons will make your work as a developer faster and easier, allowing you to concentrate on development
instead of configuration.

The addons system exposes packages, along with their versions and configuration options, in our Control Panel - you can
apply settings and manage upgrades with our GUI, not even needing to set the repository up locally to edit its code or
requirements. This can save a great deal of time, especially when a new version of a package requires different
configuration in ``settings.py``.

The Control Panel will alert you when updates are available, or in the case of critical security fixes.

The vast majority of Divio developers users prefer to make use of the framework and the wrapper applications,
though some prefer to undertake configuration manually and choose not to use it.

..  seealso::

    * :ref:`application-configuration`
    * :ref:`configure-with-aldryn-config`
    * :ref:`settings.py`
