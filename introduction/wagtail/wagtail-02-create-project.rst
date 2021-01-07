:sequential_nav: next

..  _wagtail-tutorial-set-up:

Create a new Wagtail Django project
===================================

In this section we will create and deploy a new project in the Control Panel using `Wagtail <https://wagtail.io/>`_, a
very popular Django-based content management system framework. The principles covered by the tutorial will apply to any
other development stack.

You could equally well create a plain Django project, and install Wagtail in that. However, the Wagtail project type
saves some time by setting up a ready-to-go project, with Wagtail automatically installed and configured.

..  note::

    This tutorial assumes some basic familiarity with Wagtail. It is intended to introduce the basics of working with
    the Aldryn Django framework on Divio, using Wagtail as an example. **It is not a tutorial for learning Wagtail (or
    Django)**.

    We also provide tutorials to get started with Django

    *  :ref:`from scratch <tutorial-django-set-up>`.
    *  :ref:`using the Aldryn Django framework <tutorial-aldryn-set-up>`.


..  include:: /introduction/includes/02-create-1-set-up.rst


* *Platform*: ``Python 3.x``
* *Project type*: ``Wagtail``

..  admonition:: Wagtail 2.9.2

    At the time of writing, the latest default version Aldryn Wagtail addon uses Wagtail 2.9.2 - others are also
    available.


..  include:: /introduction/includes/02-create-2-git-environments.rst

..  include:: /introduction/includes/02-create-3-deploy-open.rst


Since this is your own project, you can use our :ref:`single-sign-on <aldryn-sso>` to log in by selecting **Log in with
Divio**. You'll see the "Welcome to Wagtail" page.

More interesting are the admin pages:

* the Wagtail admin, at ``/admin``, shown below
* the Django admin, at ``/django-admin``

.. image:: /images/intro-wagtail.png
   :alt: 'Wagtail admin'
   :class: 'main-visual'


..  include:: /introduction/includes/02-create-4-deployment-dashboard.rst
