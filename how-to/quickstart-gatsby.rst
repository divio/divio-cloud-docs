..  Do not change this document name!
    Referred to by: https://github.com/divio/django-divio-quickstart
    Where:
      in the README
      in the GitHub project About field
    As: https://docs.divio.com/en/latest/how-to/quickstart-django/

.. meta::
   :description:
       The quickest way to get started with Gatsby on Divio. This guide shows you how to use the Gatsby Divio
       quickstart repository to create a Twelve-factor Gatsby project with Docker.
   :keywords: Docker, Gatsby


.. _quickstart-gatsby:

How to create a Gatsby project with our quickstart repository
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

This starts up the container with the default ``command`` in the ``docker-compose.yml`` file, which is:

..  code-block:: bash

    gatsby develop --port 80 --host 0.0.0.0

Try accessing the site at http://127.0.0.1:8000/.

If you comment out that line in ``docker-compose.yml``, it will start up with :ref:`the command specified in the
Dockerfile <deploy-gatsby-dockerfile-cmd>` instead.

You now have a working, running project ready for further development. All the commands you might normally execute
in development need to be run inside the Docker container -  prefix them with ``docker-compose run web``.


Customisation and further development
-----------------------------------------

You have multiple options for customisation. For example, this application is not configured to use a database, but if
you need to `Gatsby makes several database options possible
<https://www.gatsbyjs.com/docs/how-to/sourcing-data/sourcing-from-databases/>`_. Other customisation could include
installing additional system-level packages, Gatsby plugins and so on.

You'll need to change a few lines of configuration to achieve this across a few files. See the notes for each of:

* :ref:`the Dockerfile <deploy-gatsby-dockerfile>`
* :ref:`application configuration <deploy-gatsby-configuration>`
* :ref:`docker-compose.yml <deploy-gatsby-docker-compose>` and :ref:`.env-local <deploy-gatsby-env-local>`


Building on the host as an option
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you uncomment the:

..  code-block:: YAML

    # - ".:/app:rw"

entry in the ``web:volumes`` section of ``docker-compose.yml``, the entire ``/app`` directory will be overridden by the
project files from the host. This can be useful for development. However, you will now need to run the commands ``npm
install`` and ``gatsby build`` on the host as well in order to regenerate the files so that the container sees them.


..  include:: /how-to/includes/deploy-common-deploy.rst
