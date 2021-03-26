.. _how-to:

.. |github| image:: /images/github.png
   :alt: 'GitHub'
   :width: 28

How-to guides
=============

Working in the local development environment
--------------------------------------------

.. toctree::
    :maxdepth: 1

    Set up the Divio local development environment <local-cli>
    Run the local server in Live configuration <local-in-live-mode>


Deploy an existing web application
------------------------------------

Deploy a portable, vendor-neutral application to Divio using Docker.

.. toctree::
    :maxdepth: 1

    Deploy an application (generic guide) <deploy-generic>
    Deploy a Django application <deploy-django>
    Deploy a Flask application <deploy-flask>
    Deploy a Gatsby application <deploy-gatsby>


Create a new web application
----------------------------------------

Use one of our quickstart repositories to launch a new application from scratch in minutes.

.. toctree::
    :maxdepth: 1

    Create a Django application <quickstart-django>
    Create a django CMS application <quickstart-django-cms>
    Create a Gatsby application <quickstart-gatsby>


Building your Docker application
----------------------------------------

.. toctree::
    :maxdepth: 1

    Manage a project's base image <manage-base-image>
    Install system packages <install-system-packages>


Platform-specific guides
----------------------------------------

.. tab:: Python and Django

   .. raw:: html

      <h3>Python and Django</h3>

   For Django-based projects.

   .. toctree::
       :maxdepth: 1

       Install Python dependencies <install-python-dependencies>
       Create a multi-site Django project using Mirrors <django-multisite-mirrors>
       Go-live checklist for Django projects <live-checklist>


.. tab:: Aldryn

   .. raw:: html

      <h3>Aldryn</h3>

   For Django-based projects using the Aldryn addons framework.

   .. toctree::
       :maxdepth: 1

       Add a Django application to an Aldryn project <django-add-application>
       Configure Django settings using Aldryn <django-configure-settings>
       Configure external logging <django-configure-external-logging>
       Configure Celery <configure-celery>
       Manage access authentication <django-manage-authentication>
       Manage redirects in Django projects <django-manage-redirects>
       Log in to a local Django project <local-project-log-in>
       Manage uWSGI configuration <uwsgi-configuration>
       Fine-tune uWSGI server performance <uwsgi-performance>
       Package an application as an Aldryn addon <addon-create>
       Update an existing Aldryn addon <addon-update-existing>

.. tab:: Node.js

   .. raw:: html

      <h3>Node.js</h3>

   .. toctree::
       :maxdepth: 1

       Force HTTPS with Express.js <node-express-force-https>


-------------------------


Managing a project's resources
------------------------------

.. toctree::
    :maxdepth: 1

    Interact with your project’s database <interact-database>
    Interact with your project’s cloud media storage <interact-storage>
    Manage environment variables <environment-variables>


Adding new functionality to a project
----------------------------------------

.. toctree::
    :maxdepth: 1

    Set up Sass CSS compilation <configure-sass>
    Configure Application Performance Monitoring <configure-apm>
    Configure media serving on a custom domain <configure-media-custom-domain>


Development workflow
-------------------------

.. toctree::
    :maxdepth: 1

    Configure external Git hosting <resources-configure-git>
    Use Git to manage your project <use-git>
    Set up CI/CD <configure-ci>
    Use the Divio API <use-api>


Troubleshooting
---------------

.. toctree::
    :maxdepth: 1

    Debug cloud deployment problems <debug-deployment-problems>
    Diagnose performance issues <diagnose-performance-issues>
    Identify and resolve a Python dependency conflict <debug-dependency-conflict>
    Get help when you have a problem <debug-request-help>
