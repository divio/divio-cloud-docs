..  Do not change this document name!
    Referred to by: https://github.com/divio/django-divio-quickstart
    Where:
      in the README
      in the GitHub project About field
    As: https://docs.divio.com/en/latest/how-to/quickstart-django/

.. meta::
   :description:
       The quickest way to get started with Django on Divio. This guide shows you how to use the Django Divio
       quickstart repository to create a Twelve-factor Django project including Postgres or MySQL, and cloud media
       storage using S3, with Docker.
   :keywords: Docker, Django, Postgres, MySQL, S3


.. _quickstart-django:

How to create a Django application with our quickstart repository
=========================================================================

The `Django Divio quickstart <https://github.com/divio/django-divio-quickstart>`_ repository is a template that gives
you the fastest possible way of launching a new Django project on Divio.

It uses a completely standard Django project as created by the Django ``startproject`` management command.

The only additions are a few lines of glue code in ``settings.py`` to handle configuration using environment variables,
plus some additional files to take care of the Docker set-up.


Clone the repository
--------------------

Run:

..  code-block:: bash

    git clone git@github.com:divio/django-divio-quickstart.git

The project contains a module named ``quickstart``, containing ``settings.py`` and other project-level configuration.


..  include:: /how-to/includes/quickstart-django-customise-files.rst

..  include:: /how-to/includes/quickstart-django-common-steps.rst


Additional notes
-----------------

See :ref:`working-with-recommended-django-configuration` for further guidance.


..  include:: /how-to/includes/deploy-common-deploy.rst
