..  raw:: html

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

        .embed-responsive {
          position: relative;
          width: 100%;
        }
          .embed-responsive:before {
            display: block;
            content: "";
          }
        .embed-responsive-item,
        .embed-responsive iframe {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
        }
        .embed-responsive-16by9::before {
            padding-top: 56.25%;
        }
        .embed-responsive-4by3::before {
            padding-top: 75%;
        }

    </style>


Divio developer handbook
==============================


..  rst-class:: clearfix row

..  rst-class:: column column2


:ref:`Get started <introduction>`
-------------------------------------------------------

**Tutorials.** A hands-on introduction to Divio for developers. *Recommended for all new users.*


..  rst-class:: column column2

:ref:`How-to guides <how-to>`
-------------------------------------------------------

**Step-by-step guides.** Covers key tasks and operations and common problems.


..  rst-class:: clearfix row
..  rst-class:: column column2

:ref:`Background <background>`
-------------------------------------------------------

**Explanation.** Clarification and discussion of key topics.


..  rst-class:: column column2

:ref:`Reference <reference>`
-------------------------------------------------------

**Technical reference.** Covers tools, components, commands and resources.


Additional resources
--------------------

..  rst-class:: clearfix row

..  rst-class:: column column2

Divio Community Slack
~~~~~~~~~~~~~~~~~~~~~

The Divio Community Slack group is for all Divio users.

..  raw:: html

    <a class="btn btn-primary" target="_blank" href="https://join.slack.com/t/divio-community/shared_invite/zt-k5h56uqa-fPxLJq5vQx2OQ9xTiSJnoQ" role="button">Join the Divio Community Slack group</a>


..  rst-class:: column column2

The Divio API
~~~~~~~~~~~~~

The Divio API is a powerful tool for interacting with our infrastructure and your projects.

See:

* :ref:`use-divio-api` in this documentation
* the `Divio API reference documentation <https://api.docs.divio.com>`_


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


.. toctree::
    :maxdepth: 1
    :hidden:

    introduction/index
    how-to/index
    reference/index
    background/index
