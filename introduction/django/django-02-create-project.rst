:sequential_nav: next

..  _tutorial-django-set-up:

Create a new Django application
===============================================

..  admonition:: This is a step-by-step introduction intended for beginners.

     If you're already familiar with the basics of Divio or have experience with Docker and cloud platforms in general,
     our guide :ref:`How to create and deploy a Django application <deploy-django>` is probably more appropriate.

=============

..  sidebar:: **Have you set up the local environment?**

    If not, :ref:`do that now <tutorial-installation>` before proceeding.

In this tutorial you will create and deploy a new application using `Django <https://www.djangoproject.com/>`_, the most
popular Python web application framework. The application will be set up in Docker and integrated with various cloud
services such as database and media storage.

The principles covered by the tutorial will apply to any other development stack.


..  include:: /introduction/includes/02-create-1-set-up.rst


* *Platform*: ``Build your own``
* *Application type*: ``None``


..  include:: /introduction/includes/02-create-2-git-environments.rst


This application is empty, so though you can try deploying it, that will fail (it will fail because the deployment 
process checks for a successful start up, and so far, there isn't anything to start).


..  include:: /introduction/includes/02-create-4-deployment-dashboard.rst
