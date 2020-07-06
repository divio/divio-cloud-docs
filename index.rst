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
                width: 25%;
            }
        }

        .main-visual {
            margin-bottom: 0 !important;
        }
        h2 {border-top: 1px solid #e1e4e5; padding-top: 1em}
    </style>


Divio developer handbook
==============================

Contents
--------

.. rst-class:: clearfix row

.. rst-class:: column column2


:ref:`Tutorials <introduction>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get started with a hands-on introduction to Divio for
developers.


.. rst-class:: column column2

:ref:`How-to guides <how-to>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Step-by-step guides for the developer covering key operations and procedures


.. rst-class:: column column2

:ref:`Reference <reference>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Technical reference - tools, components and commands


.. rst-class:: column column2

:ref:`Background <background>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Explanation and discussion of key topics


.. rst-class:: clearfix row

Our development/deployment cycle in seven minutes
-------------------------------------------------------

..  raw:: html

    <iframe src="https://player.vimeo.com/video/435660924" width="758" height="474" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>


About the Divio cloud deployment platform
-----------------------------------------

`Divio <https://divio.com>`_ is a platform for containerised web
projects. Divio's cloud platform aims to offer developers:

**More reliable deployment** - it's built in Python and Django, and uses Docker
to give application developers a local development environment that is
consistent between the Cloud live and test servers - in other words, a system
where if it works on your machine, you can expect it to work in production.

**Easier deployment and maintenance** - the Dockerised Cloud platform makes it
possible for developers to get their projects online, and to take charge of
deployment, maintenance and scaling, without needing the operations or system
administrator skills this usually demands to do well.

**Better portability** - the containerisation technology used in Divio
projects guarantees portability and means freedom from lock-in to a single
provider. A Divio project can be easily deployed on another platform
that supports Docker.


Detailed table of contents
--------------------------

.. toctree::
    :maxdepth: 2

    introduction/index
    how-to/index
    reference/index
    background/index
