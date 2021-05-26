..  Do not change this document name!
    Referred to by: https://github.com/divio/php-laravel-divio-quickstart
    Where:
      in the README
      in the GitHub project About field
      in the Dockerfile
    As: https://docs.divio.com/en/latest/how-to/quickstart-php-laravel/

.. meta::
   :description:
       The quickest way to get started with Laravel on Divio. This guide shows you how to use the PHP Laravel Divio
       quickstart repository to create a Twelve-factor Laravel project including MySQL and S3 cloud media
       storage, with Docker.
   :keywords: Docker, PHP, Laravel, Postgres, MySQL, S3


.. _quickstart-php-laravel:

How to create a PHP Laravel application with our quickstart repository
=========================================================================

The `PHP Laravel quickstart <https://github.com/divio/php-laravel-divio-quickstart>`_ repository is a template that
gives you the fastest possible way of launching a new Laravel project on Divio.

It's based on Laravel's own example project. The only additions are some glue code to handle configuration using
environment variables, plus some additional files to take care of the Docker set-up.


Clone the repository
--------------------

Run:

..  code-block:: bash

    git clone git@github.com:divio/php-laravel-divio-quickstart.git

You'll find a directory named ``divio`` containing some helper modules scripts and modules, that are used (for
example) to read the environment variables we provide to configure database and media storage.


Run the project locally
-----------------------

This section assumes that you have Docker and the Divio CLI installed. You also need an account on Divio, and your
account needs your SSH public key. See :ref:`local-cli` if required.


Build the Docker image
~~~~~~~~~~~~~~~~~~~~~~

Run:

..  code-block:: bash

    docker-compose build


Run database migrations
~~~~~~~~~~~~~~~~~~~~~~~

First, open a bash shell in a local container:

..  code-block:: bash

    docker-compose run web bash

Then, in the shell run migrations using Artisan:

..  code-block:: bash

    php artisan migrate

..  admonition:: MySQL errors

    An error can occur if the the MySQL service has failed to start up in time::

         Illuminate\Database\QueryException

        SQLSTATE[HY000] [2002] Connection refused [...]

    In this case, wait a few moments and run the command again.

Then exit the shell.


Launch the local server
~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: bash

    docker-compose up

This starts up the container with the default ``command`` in the ``docker-compose.yml`` file, which is:

..  code-block:: bash

    bash -c "chmod a+x /app/divio/run-locally.sh && php /app/divio/run-env.php /app/divio/run-locally.sh"

Try accessing the site at http://127.0.0.1:8000/.

If you comment out that line in ``docker-compose.yml``, it will start up with the command specified in the
``Dockerfile`` instead.

You now have a working, running project ready for further development. All the commands you might normally execute
in development need to be run inside the Docker container -  prefix them with ``docker-compose run web``.


.. _quickstart-php-laravel-mapping-to-the-host:

Mapping ``/app`` to the local host filesystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The host/container volume mapping directive in the ``docker-compose.yml`` file is commented out by default:

..  code-block:: YAML

    # - ".:/app:rw"

If you uncomment this entry, the entire ``/app`` directory inside the container will be overridden by the project files
from the host when using Docker Compose. This can be useful for development.

However you will now need to re-run any commands in the ``Dockerfile`` that change items within the ``/app`` directory
as part of the build process, otherwise the file changes made by ``Dockerfile`` operations in the image will not be
reflected in the container.

For convenience, all these commands are included in the ``setup.sh`` file. If you do need to map ``/app`` to the host
filesystem, run:

..  code-block:: bash

    docker-compose run web sh setup.sh

after any ``docker-compose build`` operations.


Launching the local server with nginx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Dockerfile`` launches the server with nginx:

..  code-block:: Dockerfile

    CMD php /app/divio/run-env.php "/usr/bin/dumb-init nginx && php-fpm -R"

However when you start a local instance with ``docker-compose up``, it uses the ``command`` in ``docker-compose.yml``
instead:

..  code-block:: Dockerfile

    command: bash -c "chmod a+x /app/divio/run-locally.sh && php /app/divio/run-env.php /app/divio/run-locally.sh"

Comment this out to use nginx locally with Docker Compose.


..  include:: /how-to/includes/deploy-common-deploy.rst
