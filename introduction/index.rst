..  Do not change this document name!
    Referred to by: Aldryn django CMS repository
    Where: https://github.com/divio/aldryn-django-cms/readme.rst
    Referred to by: Intercom welcome message
    Where: https://app.intercom.com/a/apps/wcfe7111/outbound/messages/auto/354454445
    As: https://docs.divio.com/en/latest/introduction


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
    </style>


.. _introduction:

Tutorial
=========

About the tutorial
------------------

..  admonition:: Prerequisites

    The tutorial assumes you are comfortable with the command line, and understand the basics of using SSH keys, Git
    and so on.

    **Not a developer?** If you would like a quick overview of the Divio platform features and interface, see our
    short video `Web project management with Divio <https://www.divio.com/demo/watch/?video=management>`_.


The tutorial will introduce you to the Divio toolchain, and the complete cycle of project creation, development,
deployment and management as a Developer, from setting up a project locally to deploying your own application on the
cloud.


Choose your pathway
-------------------

We offer multiple pathways though the tutorial. In each case, the same principles will be used for any language you use
for your applications on Divio. We recommend starting with one of these tutorials even if you plan to work with a
different language later, as the tutorials have been designed to help you become familiar with key when working with
Divio.


The tutorials
------------------

**Before you do anything else, start here.** The local development environment is where you'll be doing most of your
work.

..  toctree::
    :maxdepth: 1

    01-installation


Next, select your path through the tutorial.

..  What follows is a terrible hack to force the behaviour we want from Sphinx. It could end badly. See hacks.rst for
    more.

..  raw:: html

    <div class="tabs">
      <div class="tabs__nav">
         <a href="#django-tab" class="tabs__link tab__link--active">
           <img src="../_images/django-logo-negative.svg" alt="Django" width="60">
         </a>
         <a href="#aldryn-tab" class="tabs__link tab__link--active">
           Django, using Aldryn
         </a>
         <a href="#wagtail-tab" class="tabs__link tab__link--active">
           <img src="../_images/wagtail-logo.svg" alt="Wagtail" width="60"></a>
         </a>
         <a href="#php-laravel-tab" class="tabs__link">
           <img src="../_images/laravel-logo.svg" alt="Laravel" width="60"> (beta)</a>
        </a>
      <div>
      <div class="tabs__content">


.. _django:

.. rst-class:: tabs-pane

Django
~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    django-02-create-project
    django-03-setup-project-locally.rst
    django-04-deploy
    django-05-services
    django-06-refinements.rst


.. _aldryn-django-chapters:

.. rst-class:: tabs-pane

Django, using Aldryn
~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    aldryn-django-02-create-project
    aldryn-django-03-setup-project-locally.rst
    aldryn-django-04-add-application
    aldryn-django-05-more-complex-configuration


.. _wagtail:

.. rst-class:: tabs-pane

Wagtail
~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    wagtail-02-create-project
    wagtail-03-setup-project-locally
    wagtail-04-add-application


.. |flavours| image:: /images/flavours.svg
   :width: 9


.. _php-laravel:

.. rst-class:: tabs-pane

PHP/Laravel, using Flavours
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 1

    laravel-02-create-project
    laravel-03-setup-project-locally
    laravel-04-add-application
    laravel-05-flavours


.. raw:: html

    </div><!-- .tabs__content -->
    </div><!-- .tabs -->
