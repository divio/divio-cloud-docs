.. meta::
   :description:
       This guide explains step-by-step how to deploy a Laravel application with Docker, in accordance with
       Twelve-factor principles.
   :keywords: Docker, Postgres, MySQL, S3

..  _deploy-laravel:

How to deploy a Laravel web application on Divio
===========================================================================================

..  include:: /how-to/includes/deploy-common-intro.rst

The application described here is based on Laravel's own example application.

..  include:: /how-to/includes/deploy-common-prerequisites.rst

..  include:: /how-to/includes/deploy-common-dockerfile.rst

For this example we will use:

..  code-block:: Dockerfile

    FROM php:7.3-fpm-stretch

This image includes the `FastCGI Process Manager for PHP <https://php-fpm.org>`_ - there are other ways to deploy PHP.
We cannot advise on what base image you should use; you'll need to use one that is in-line with your application's
needs.

..  include:: /how-to/includes/deploy-common-dockerfile-base-images.rst

..  include:: /how-to/includes/deploy-common-dockerfile-system-dependencies.rst

In this case, a good starting set is:

..  code-block:: Dockerfile

    RUN apt-get update && apt-get install -y gnupg gosu curl ca-certificates zip unzip git supervisor mysql-client nginx dumb-init

In addition, some convenience Docker PHP binaries are available:

..  code-block:: Dockerfile

    RUN docker-php-ext-install mbstring pdo pdo_mysql

..  include:: /how-to/includes/deploy-common-dockerfile-working-directory.rst

This example uses nginx as a server;

..  code-block:: Dockerfile

    COPY divio/nginx/vhost.conf /etc/nginx/sites-available/default


..  include:: /how-to/includes/deploy-common-dockerfile-application-dependencies.rst

First, set the ``Dockerfile`` to  install Composer itself, and then run the ``composer install`` command:

..  code-block:: Dockerfile

    RUN php -r "readfile('http://getcomposer.org/installer');" | php -- --install-dir=/usr/bin/ --filename=composer
    RUN composer install --no-scripts --no-autoloader

Composer will expect to read the dependencies from ``composer.json`` or ``composer.lock`` - you will need to have
one in the application.

..  include:: /how-to/includes/deploy-common-dockerfile-file-building.rst

..  include:: /how-to/includes/deploy-common-dockerfile-cmd.rst

..  todo::

    Add a note and example of how to start the application with CMD [required]

..  include:: /how-to/includes/deploy-common-cmd-admonition.rst

..  include:: /how-to/includes/deploy-common-dockerfile-access-services.rst

..  include:: /how-to/includes/deploy-common-configuration-services.rst

..  include:: /how-to/includes/deploy-common-helper-modules.rst

..  todo::

    Add a note and example about helper modules [required]

..  include:: /how-to/includes/deploy-common-settings-security.rst

..  todo::

    Add a note and example about security settings [recommended]

..  include:: /how-to/includes/deploy-common-settings-database.rst

..  todo::

    Add a note and example about database settings [recommended]

..  include:: /how-to/includes/deploy-common-settings-static.rst

..  todo::

    Add a note and example about static serving settings, including advice [recommended]

..  include:: /how-to/includes/deploy-common-settings-media.rst

..  todo::

    Add a note and example about media serving settings; link to :ref:`how we recommend using the DEFAULT_STORAGE_DSN
    in a Django application <deploy-django-media>` if you don't have a good example [recommended]

..  include:: /how-to/includes/deploy-common-settings-media-admonition.rst

..  include:: /how-to/includes/deploy-common-settings-other.rst

..  todo::

    Mention any other steps required to provide a complete solution e.g. for local media file serving [recommended]

..  include:: /how-to/includes/deploy-common-compose.rst

..  todo::

    Provide an example docker-compose.yml, emphasising lines the user must pay attention to. See examples from other
    guides [required]

..  include:: /how-to/includes/deploy-common-compose-env-local.rst

..  todo::

    Provide an example .env-local, emphasising lines the user must pay attention to. See examples from other
    guides, including the deploy-generic guide [required]

..  include:: /how-to/includes/deploy-common-compose-summary.rst

..  include:: /how-to/includes/deploy-common-buildrun-build.rst

..  todo::

    Add a note and examples about key steps required here, e.g. migrations, creating a superuser, etc. See the
    deploy-django guide for an example [required]

..  include:: /how-to/includes/deploy-common-buildrun-run.rst

..  include:: /how-to/includes/deploy-common-git.rst

..  todo::

    Add some suggested entries for ``.gitignore`` [required]

..  include:: /how-to/includes/deploy-common-deploy.rst

..  todo::

    Add a final section with a first-level heading about what to do or read next [recommended]
