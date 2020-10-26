:sequential_nav: next

..  _tutorial-aldryn-set-up:

Create a new Django project using Aldryn Django
===============================================

About this tutorial
-------------------

In this tutorial you will create and deploy a new project using Aldryn Django. Aldryn is a wrapper around `Django
<https://www.djangoproject.com/>`_, the most popular Python web application framework. Aldryn provides automatic
configuration and integration with cloud services such as database, media storage and so on.

..  important::

    Unless you are sure you wish to use Aldryn, we recommend starting with :ref:`our standard Django tutorial
    <tutorial-django-set-up>` instead.


..  include:: includes/02-create-1-set-up.rst


* *Platform*: ``Python 3.x``
* *Project type*: ``Django``

..  admonition:: Django 2.2

    At the time of writing, version 2.2 is `Django's Long-Term Support release
    <https://www.djangoproject.com/download/#supported-versions>`_, and is
    guaranteed support until at least April 2022. This is the version currently
    selected by default in Divio projects.


..  include:: includes/02-create-2-git-environments.rst

..  include:: includes/02-create-3-deploy-open.rst


Since this is your own project, you can use our :ref:`single-sign-on <aldryn-sso>` to log in by selecting **Log in with
Divio**. You'll see the familiar Django admin for a new project.

.. image:: /images/intro-django-admin.png
   :alt: 'Django admin'
   :class: 'main-visual'


..  include:: includes/02-create-4-deployment-dashboard.rst
