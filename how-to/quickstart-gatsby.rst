..  Do not change this document name!
    Referred to by: https://github.com/divio/django-divio-quickstart
    Where:
      in the README
      in the GitHub project About field
    As: https://docs.divio.com/en/latest/how-to/django-deploy-quickstart/

.. meta::
   :description:
       The quickest way to get started with Gatsby on Divio. This guide shows you how to use the Gatsby Divio
       quickstart repository to deploy a Twelve-factor Gatsby project including with Docker.
   :keywords: Docker, Gatsby


.. gatsby-deploy-quickstart:

How to deploy a Gatsby project with our quickstart repository
=========================================================================

The `Gatsby Divio quickstart <https://github.com/divio/gatsby-divio-quickstart>`_ repository is a template that gives
you the fastest possible way of launching a new Gatsby project on Divio.

It uses a completely standard Gatsby project as used in the `Gatsby Hello World boilerplate
<https://github.com/gatsbyjs/gatsby-starter-hello-world/blob/master/README.md>`_.

The repository contains some additional files to take care of the Docker set-up.


Clone the repository
--------------------

Run:

..  code-block:: bash

    git clone git@github.com:divio/gatsby-divio-quickstart.git

The project contains a module named ``quickstart``, containing ``settings.py`` and other project-level configuration.


Run the project locally
-----------------------

This section assumes that you have Docker and the Divio CLI installed. You also need an account on Divio, and your
account needs your SSH public key. See :ref:`local-cli` if required.


Build the Docker image
~~~~~~~~~~~~~~~~~~~~~~

Run:

..  code-block:: bash

    docker-compose build


Launch the local server
~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: bash

    docker-compose up

Try accessing the site at http://127.0.0.1:8000/.

You now have a working, running project ready for further development. All the commands you might normally execute
in development need to be run inside the Docker container -  prefix them with ``docker-compose run web``.

..  include:: /how-to/includes/deploy-common-deploy.rst


Customisation and further development
-----------------------------------------

You have multiple options for customisation. For example, this application is not configured to use a database, but if
you need to `Gatsby makes several database options possible
<https://www.gatsbyjs.com/docs/how-to/sourcing-data/sourcing-from-databases/>`_. Other customisation could include
installing additional system-level packages, Gatsby plugins and so on.

You'll need to change a few lines of configuration to achieve this across a few files. See the notes for each:

* :ref:`the Dockerfile <deploy-gatsby-dockerfile>`
* :ref:`application configuration <deploy-gatsby-configuration>`
* :ref:`docker-compose.yml <deploy-gatsby-docker-compose>` and :ref:`.env-local <deploy-gatsby-env-local>`
