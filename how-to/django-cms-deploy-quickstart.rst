..  Do not change this document name!
    Referred to by: https://github.com/divio/django-cms-divio-quickstart
    Where:
      in the README
      in the GitHub project About field
    As: https://docs.divio.com/en/latest/how-to/django-cms-deploy-quickstart/

.. meta::
   :description:
       The quickest way to get started with django CMS on Divio. This guide shows you how to use the django CMS Divio
       quickstart repository to deploy a Twelve-factor django CMS project including Postgres or MySQL, and cloud media
       storage using S3, with Docker.
   :keywords: Docker, Django, django CMS, Postgres, MySQL, S3


.. _django-cms-deploy-quickstart:

How to deploy a new django CMS project using the Divio quickstart repository
=============================================================================

The `django CMS Divio quickstart <https://github.com/divio/django-cms-divio-quickstart>`_ repository is a template that
gives you the fastest possible way of launching a new django CMS project on Divio.

It uses a standard, minimal django CMS project as modelled on that created by the django CMS installer.

The only additions are a few lines of glue code in ``settings.py`` to handle configuration using environment variables,
plus some additional files to take care of the Docker set-up.

The project includes some (clearly-indicated) options for popular components (such as Django Filer) and also a
Bootstrap 4 frontend. These can quickly be removed if you prefer a more minimal project to work with.

Clone the repository
--------------------

Run:

..  code-block:: bash

    git clone git@github.com:divio/django-cms-divio-quickstart.git

The project contains a module named ``quickstart``, containing ``settings.py`` and other project-level configuration.


Removing optional components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``settings.py`` and ``requirements.txt`` files contain sections that can be removed if you do not require the
functionality they provide - in each case, the section is noted with a comment containing the word *optional*. You will
need to make sure that you remove the corresponding sections from both files if you do.

The options include:

* components typically used with django CMS (CKEditor, Django File, django CMS Admin Style)
* some popular basic content plugins
* components and templates required for a Bootstrap 4 frontend


..  include:: /how-to/includes/django-deploy-quickstart-customise-files.rst

..  include:: /how-to/includes/django-deploy-quickstart-common-steps.rst
