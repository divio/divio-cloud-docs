.. _how-to:

How-to guides
=============

Working in the local development environment
--------------------------------------------

.. toctree::
    :maxdepth: 1

    Get started with the Divio CLI <local-cli>
    Run the local server in Live mode <local-in-live-mode>


Building your Docker application
----------------------------------------

.. toctree::
    :maxdepth: 1

    Manage a project's base image <manage-base-image>
    Install system packages <install-system-packages>


Adding new functionality to a project
----------------------------------------

.. toctree::
    :maxdepth: 1

    Set up Sass CSS compilation <configure-sass>
    Configure Application Performance Monitoring <configure-apm>


Platform-specific guides
----------------------------------------

..  What follows is a terrible hack to force the behaviour we want from Sphinx. It could end badly. See hacks.rst for
    more.

.. raw:: html

    <div class="tabs">
      <div class="tabs__nav">
         <a href="#python-tab" class="tabs__link tab__link--active">
           <img src="../_images/python-logo.svg" alt="Python" width="80">
         </a>
         <a href="#django-tab" class="tabs__link">
           <img src="../_images/django-logo-negative.svg" alt="Django" width="60">
         </a>
         <a href="#node.js-tab" class="tabs__link">
           <img src="../_images/node-logo.svg" alt="Node.js" width="60">
         </a>
      <div>
      <div class="tabs__content">


.. rst-class:: tabs-pane

Python
~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    Install Python dependencies <install-python-dependencies>
    Pin all of your project's Python dependencies <resources-pin-dependencies>


.. rst-class:: tabs-pane

Django
~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    Add a Django application <django-add-application>
    Configure Django settings <django-configure-settings>
    Migrate an existing Django project to Divio <django-migrate-existing-project>
    Create a multi-site Django project using Mirrors <django-multisite-mirrors>
    Configure external logging <django-configure-external-logging>
    Configure Celery <configure-celery>
    Set up password protection <password-protect-project>
    Log in to a local Django project <local-project-log-in>


.. rst-class:: tabs-pane

Node.js
~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    Force HTTPS with Express.js <node-express-force-https>

.. raw:: html

    </div><!-- .tabs__content -->
    </div><!-- .tabs -->


The development pipeline
-------------------------

.. toctree::
    :maxdepth: 1

    Configure external Git hosting <resources-configure-git>
    Use Git to manage your project <use-git>
    Set up CI/CD <configure-ci>
    Use our API <use-api>


Managing a project's resources
------------------------------

.. toctree::
    :maxdepth: 1

    Interact with your project’s database <interact-database>
    Interact with your project’s media storage <interact-storage>


Working with addons
-------------------

.. toctree::
    :maxdepth: 1

    Package an application as an addon <create-addon>
    Update an existing addon <update-existing-addon>


Going live and maintaining performance
--------------------------------------

.. toctree::
    :maxdepth: 1

    Go-live checklist <live-checklist>
    Fine-tune uWSGI server performance <live-performance>


Troubleshooting
---------------

.. toctree::
    :maxdepth: 1

    Debug cloud deployment problems <debug-deployment-problems>
    Identify and resolve a Python dependency conflict <debug-dependency-conflict>
    Get help when you have a problem <debug-request-help>
