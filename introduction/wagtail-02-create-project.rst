..  _wagtail-tutorial-set-up:

Create a new Wagtail Django project
===================================

In this section we will create and deploy a new project in the Control Panel using `Wagtail <https://wagtail.io/>`_, a
very popular Django-based content management system framework. (You don't need to know Wagtail, Django or Python, or
have them installed on your system.) The principles covered by the tutorial will apply to any other development stack.

You could equally well create a plain Django project, and install Wagtail in that. However, the Wagtail project type
saves some time by setting up a ready-to-go project, with Wagtail automatically installed and configured.


..  include:: includes/set-up-project.rst


* *Python*: ``Python 3.x``
* *Project type*: ``Wagtail``

..  admonition:: Wagtail 2.9.2

    At the time of writing, the latest default version Aldryn Wagtail addon uses Wagtail 2.9.2 - others are also
    available.


..  include:: includes/set-up-project-cont.rst


Since this is your own project, you can use our :ref:`single-sign-on <aldryn-sso>` to log in by selecting **Log in with
Divio**. You'll see the "Welcome to Wagtail" page.

More interesting are the admin pages:

* the Wagtail admin, at ``/admin``, shown below
* the Django admn, at ``/django-admin``

.. image:: /images/intro-wagtail.png
   :alt: 'Wagtail admin'
   :class: 'main-visual'


..  include:: includes/deployment-dashboard.rst
