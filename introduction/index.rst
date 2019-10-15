.. raw:: html

    <style>
        .row {clear: both}

        .column img {border: 1px solid black;}

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

.. rst-class:: clearfix row

.. rst-class:: column column2

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


.. rst-class:: column column2

PHP/Lavarel, using Flavours
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    flavours-php-set-up
    flavours-php-add-application
