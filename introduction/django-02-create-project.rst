..  _tutorial-django-set-up:

Create a new Django project from scratch
===============================================

In this tutorial you will create and deploy a new project using `Django <https://www.djangoproject.com/>`_, the most
popular Python web application framework. The project will be set up in Docker and integrated with various cloud
services such as database and media storage.

The principles covered by the tutorial will apply to any other development stack.

..  note::

    This tutorial is intended to introduce the basics of working with Divio, using Django as an example. **It is not a
    tutorial for Django**.


..  include:: includes/02-create-1-set-up.rst


* *Platform*: ``No platform``
* *Project type*: ``Empty``


..  include:: includes/02-create-2-git-environments.rst


This project is empty, so though you can try deploying it, that will fail (it will fail because the deployment process
checks for a successful start up, and so far, there isn't anything to start).


..  include:: includes/02-create-4-deployment-dashboard.rst
