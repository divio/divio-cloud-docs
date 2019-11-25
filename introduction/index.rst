.. raw:: html

    <style>
        .row {clear: both}

        @media only screen and (min-width: 1000px),
               only screen and (min-width: 500px) and (max-width: 768px){

            .column {
                padding-left: 5px;
                padding-right: 5px;
                float: left;
            }

            .column2  {
                width: 50%;
            }
        }

        .main-visual {
            margin-bottom: 0 !important;
        }
        h2 {border-top: 1px solid #e1e4e5; padding-top: 1em}
    </style>


.. _introduction:

Tutorials
=========

These tutorials are suitable for developers. They assume that you are reasonably familiar with
using the command line for development work, and that you know how to use and manage things such as
Git, Pip and SSH keys.

The tutorials will take you through a complete cycle of operations as a Divio Cloud developer, from setting up a
project locally to deploying your own applications on the Cloud.


Get started
-----------

Create an account and set up your local environment.

.. toctree::
    :maxdepth: 1

    01-installation


Learn the development and deployment workflow
----------------------------------------------------

.. raw:: html

    <div class="tabs">
      <div class="tabs__nav">
         <a href="#django-using-aldryn" class="tabs__link tab__link--active">Django</a>
         <a href="#php-lavarel-using-flavours-flavours" class="tabs__link">PHP, Laravel</a>
      <div>
      <div class="tabs__content">

.. rst-class:: tabs-pane

Django, using Aldryn
~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    02-set-up-django
    Add new applications <03-add-applications>
    04-addon-configuration
    05-package-addon
    06-package-addon-configuration
    07-package-addon-cloud
    08-create-custom-boilerplate
    09-migrate-project


.. |flavours| image:: /images/flavours.svg
   :width: 9


.. rst-class:: tabs-pane

PHP/Lavarel, using Flavours |flavours|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Access to Flavours on Divio is currently in a *private beta* phase. Sign up for access via `the Flavours website
<https://www.flavours.dev>`_.

.. toctree::
    :maxdepth: 1

    flavours-php-set-up
    flavours-php-add-application

.. raw:: html

    </div><!-- .tabs__content -->
    </div><!-- .tabs -->
