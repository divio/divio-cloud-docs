:orphan:

.. meta::
   :description:
       This guide explains step-by-step how to deploy a application with Docker, in accordance with
       Twelve-factor principles.
   :keywords: Docker, Postgres, MySQL, S3


How to deploy an application on Divio: template
===========================================================================================

..  include:: /how-to/includes/deploy-common-intro.rst

..  todo::

    Add a note about scope and about other guides [recommended]

..  include:: /how-to/includes/deploy-common-prerequisites.rst

..  include:: /how-to/includes/deploy-common-dockerfile.rst

..  todo::

    Add a note about base images [required] - example:

    For a Python application, use the following:

    ..  code-block:: Dockerfile

        FROM python:3.8

    Here, ``python:3.8`` is the name of the Docker *base image*. We cannot advise on what base image you should use;
    you'll need to use one that is in-line with your application's needs. However, once you have a working set-up, it's
    good practice to move to a more specific base image - for example ``python:3.8.1-slim-buster``.

    ..  seealso::

        * :ref:`manage-base-image-choosing`
        * `Divio base images on Docker Hub <https://hub.docker.com/r/divio/base/tags?page=1&ordering=last_updated>`_

..  include:: /how-to/includes/deploy-common-dockerfile-system-dependencies.rst

..  include:: /how-to/includes/deploy-common-dockerfile-working-directory.rst

..  todo::

    Add a note on working directories [recommended]

..  include:: /how-to/includes/deploy-common-dockerfile-application-dependencies.rst

..  todo::

    Add a note about pinning dependencies; list any known required dependencies [required] - example:

    ..  code-block:: Dockerfile

        # install dependencies listed in the repository's requirements file
        RUN pip install -r requirements.txt

    Any requirements should be pinned as firmly as possibble.


..  include:: /how-to/includes/deploy-common-dockerfile-file-building.rst

..  todo::

    Add a note and example of file-building for this framework [recommended]

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

    Provide an example .env_local, emphasising lines the user must pay attention to. See examples from other
    guides, including the deploy-generic guide [required]

..  include:: /how-to/includes/deploy-common-compose-summary.rst

..  include:: /how-to/includes/deploy-common-buildrun-build.rst

..  todo::

    Add a note and examples about key steps required here, e.g. migrations, creating a superuser, etc. See the
    deploy-django guide for an example [required]

..  include:: /how-to/includes/deploy-common-buildrun-run.rst

..  include:: /how-to/includes/deploy-common-git.rst

..  todo::

    Add some suggested entried for .gitignore [required]

..  include:: /how-to/includes/deploy-common-deploy.rst

..  todo::

    Add a final section with a first-level heading about what to do or read next [recommended]
