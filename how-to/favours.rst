How to get started with Flavours
================================

Flavours is a platform-independent specification for building containerised web projects. This section describes
how to get started with Divio's implementation of Flavours.

Flavours:

* acts on a repository of files (whether locally, or on a remote host)
* communicates with a registry of images

Examples of things you can do with Flavours:

* create a new web project, ready for Cloud deployment, with a single command
* add and remove components in a Flavours-aware project

Install the Divio Flavours CLI
------------------------------

* The source is available at source https://gitlab.com/divio/flavour/cli
* Install: ``npm install -g @flavour/cli``




getting started project https://gitlab.com/divio/flavour/getting-started/diviocloud-addon-getting-started

https://hub.eu.aldryn.io



10245* flavour check
10274* flavour --help
10275* flavour add addons/aldryn-redirects
10276* flavour --help
10277* flavour add --help
10278* flavour add --no-cache addons/aldryn-redirects
10281* flavour add addons/aldryn-redirects
10282* flavour add helloworld/bash
10284* flavour add helloworld/bash
10289* flavour add divio/django-cloud-essentials-storage
10291* flavour add divio/django-cloud-essentials-storage
10292* flavour add --no-check divio/django-cloud-essentials-storage
10296* flavour add composer/barryvdh/laravel-debugbar
10328* flavour add addons/aldryn-redirect
10329* flavour add --no-cache addons/aldryn-redirects
10330* flavour remove --no-cache addons/aldryn-redirects
10331* flavour remove --no-cache addons/aldryn-django
10332* flavour add addons/aldryn-django
10333* flavour remove --no-cache addons/aldryn-django
10334* flavour remove --no-cache addons/aldryn-addons


what makes a project flavours-aware?
====================================

* flavour.yml locally
* will become app.flavour
* on the cloud?


interaction with Aldryn addons framework
========================================

* e.g. https://gitlab.com/divio/flavour/getting-started/diviocloud-addon-getting-started project



examples of using the system to achieve some everyday tasks
===========================================================




examples of using the system to create and manage some custom code that others will use
========================================================================================


migrating an existing addon over to support flavours
===========================================================


create a new platform (not super simple but also not too hard)
==============================================================



flavours CLI reference
======================


divio project up - looks at app.flavour and follows instructions to build dc etc.