..  Do not change this document name!
    Referred to by: Aldryn django CMS repository
    Where: https://github.com/divio/aldryn-django-cms/readme.rst
    As: https://docs.divio.com/en/latest/background/addon-basics

.. _aldryn:

About Aldryn (legacy)
==================================

..  note:: Aldryn continues to be supported by Divio, but we do not recommend using Aldryn Django for new applications.

The :ref:`Aldryn Django addons framework <aldryn-addons>` is an optional system that allows packages to be installed and
configured very easily and in some cases fully automatically.


What are Aldryn addons?
-----------------------

Addons can be thought of as wrappers for Python packages such as Django or django CMS that allow them to take advantage
of our addons framework. You'll see for example addons such as Aldryn Django (a wrapper/installer for Django) and
Aldryn Django CMS (a wrapper/installer for django CMS).

Aldryn Addons are provided as a convenience. If you'd like Django in your project, with all its settings configured for our
infrastructure (uWSGI gateway, database, media storage etc), and in such a way that they will work correctly in the
Live, Test and local environments, then Aldryn Django will take care of that for you; if it's installed, all that
configuration and wiring will be done automatically.

In the case of Aldryn Django CMS, it will configure settings such as ``MIDDLEWARE`` and ``TEMPLATES`` automatically.

Packages as installed by Divio addons (such as Django or django CMS) are **completely standard and unmodified**.

Installation and basic configuration of addons is managed via the project's dashboard in the Control Panel. More advanced configuration can be managed via :ref:`settings <how-to-settings>` and :ref:`environment variables <environment-variables>`.


Using Aldryn is optional
-------------------------

Using the Aldryn framework on Divio is completely optional.

You don't *need* Aldryn Django to install or use Django. Similarly, django CMS can be installed and configured
manually, without using Aldryn Django CMS, if you prefer, and the same goes for others.
