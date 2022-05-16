..  Do not change this document name!
    Referred to by: https://github.com/divio/django-cms-divio-quickstart
    Where:
      in the README
      in the GitHub application About field
    As: https://docs.divio.com/en/latest/how-to/django-cms-deploy-quickstart/

.. meta::
   :description:
       The quickest way to get started with django CMS on Divio. This guide shows you how to use the django CMS Divio
       quickstart repository to create a Twelve-factor django CMS application including Postgres or MySQL, and cloud media
       storage using S3, with Docker.
   :keywords: Docker, Django, django CMS, Postgres, MySQL, S3


.. _django-cms-deploy-quickstart:

How to create a django CMS application with our quickstart repository
=============================================================================

The `django CMS Divio quickstart <https://github.com/divio/django-cms-divio-quickstart>`_ repository is a template that
gives you the fastest possible way of launching a new django CMS application on Divio.

It uses a standard, minimal django CMS application as modelled on that created by the django CMS installer.

The only additions are a few lines of glue code in ``settings.py`` to handle configuration using environment variables,
plus some additional files to take care of the Docker set-up.

The application includes some (clearly-indicated) options for popular components (such as Django Filer) and also a
Bootstrap 4 frontend. These can quickly be removed if you prefer a more minimal application to work with.

Clone the repository
--------------------

Run:

..  code-block:: bash

    git clone git@github.com:divio/django-cms-divio-quickstart.git

The application contains a module named ``quickstart``, containing ``settings.py`` and other application-level 
configuration.


Removing optional components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``settings.py`` and ``requirements.txt`` files contain sections that can be removed if you do not require the
functionality they provide - in each case, the section is noted with a comment containing the word *optional*. You will
need to make sure that you remove the corresponding sections from both files if you do.

The options include:

* components typically used with django CMS (CKEditor, Django File, django CMS Admin Style)
* some popular basic content plugins
* components and templates required for a Bootstrap 4 frontend


..  include:: /how-to/includes/quickstart-django-customise-files.rst

..  include:: /how-to/includes/quickstart-django-common-steps.rst


Additional notes
-----------------

See :ref:`working-with-recommended-django-configuration` for further guidance.


..  include:: /how-to/includes/deploy-common-deploy.rst
