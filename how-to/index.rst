.. _how-to:

.. |github| image:: /images/github.png
   :alt: 'GitHub'
   :width: 28

How-to guides
=============

.. _how-to-existing-web-application:

Configure an existing web application for deployment
----------------------------------------------------

Prepare your web application for deployment on Divio with Docker.

.. toctree::
    :maxdepth: 1

    Configure an application (generic guide) <deploy-generic>
    Configure a Django application <deploy-django>
    Configure a Flask application <deploy-flask>
    Configure a Gatsby application <deploy-gatsby>


.. _how-to-use-quickstart:

Create a new application
----------------------------------------

Use one of our quickstart repositories to create a new deployment-ready application from scratch in a few minutes.

.. toctree::
    :maxdepth: 1

    Start a Django application <quickstart-django>
    Start a django CMS application <quickstart-django-cms>
    Start a Gatsby application <quickstart-gatsby>
    Start a PHP Laravel application <quickstart-php-laravel>


Deploy an application
----------------------

.. toctree::
    :maxdepth: 1

    Deploy your application to the Divio cloud platform <deploy>
    Go-live checklist <live-checklist>


Development workflow
-------------------------

.. toctree::
    :maxdepth: 1

    Set up the Divio local development environment <local-cli>
    Run a local application in live configuration <local-in-live-configuration>
    Configure external Git hosting <resources-configure-git>
    Use Git to manage your project <use-git>
    Set up CI/CD <configure-ci>
    Use the Divio API <use-api>


Building a Docker application
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
       Configure Celery <configure-celery>


.. tab:: Node.js

   .. raw:: html

      <h3>Node.js</h3>

   .. toctree::
       :maxdepth: 1

       Force HTTPS with Express.js <node-express-force-https>


.. tab:: Aldryn (legacy)

   .. raw:: html

      <h3>Aldryn</h3>

   For Django-based projects using the Aldryn addons framework.

   .. toctree::
       :maxdepth: 1

       Add a Django application to an Aldryn project <django-add-application>
       Configure Django settings using Aldryn <django-configure-settings>
       Configure external logging <django-configure-external-logging>
       Manage access authentication <django-manage-authentication>
       Manage redirects in Django projects <django-manage-redirects>
       Log in to a local Django project <local-project-log-in>
       Manage uWSGI configuration <uwsgi-configuration>
       Fine-tune uWSGI server performance <uwsgi-performance>
       Package an application as an Aldryn addon <addon-create>
       Update an existing Aldryn addon <addon-update-existing>

-------------------------


Managing a project's resources
------------------------------

.. toctree::
    :maxdepth: 1

    Interact with your project’s database <interact-database>
    Interact with your project’s cloud media storage <interact-storage>
    Configure media serving on a custom domain <configure-media-custom-domain>
    Manage environment variables <environment-variables>


Troubleshooting
---------------

.. toctree::
    :maxdepth: 1

    Debug cloud deployment problems <debug-deployment-problems>
    Diagnose performance issues <diagnose-performance-issues>
    Identify and resolve a Python dependency conflict <debug-dependency-conflict>
    Get help when you have a problem <debug-request-help>
