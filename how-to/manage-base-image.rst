.. _manage-base-image:

How to manage a project's base image
=========================================================

Divio provides a number of `Docker base images for projects
<https://hub.docker.com/r/divio/base/tags>`_. These base images provide an underlying Linux
operating system layer, and other layers in the stack, upon which you can build your custom
application.

For example, our Python base images will include a particular version of Python, and any
system-level components required to run it.

New base images will be released with updates (for example, for newer Python releases) and other
improvements or changes. Generally, it's recommended to use the newest version of the base image
in a particular *Release Channel*.

A project's Release Channel is indicated in its Dashboard, in *Settings* > *Base Project*. Note
however that because the base image can also be specified in the repository via the ``Dockerfile``,
the manual setting will override what's indicated in the Dashboard.

This document is concerned with using the ``Dockerfile`` to manage the base image.


Choose a base image
-------------------

You don't need to use a Divio-provided base image. However, it's recommended.

Our base images are listed on `Docker Hub <https://hub.docker.com/r/divio/base/tags>`_.

Your base image should include the runtime environment(s) you need for your application, such as
an appropriate version of Python.


Specify the base image in the ``Dockerfile``
--------------------------------------------

For example, to use our ``0.4-py3.7-slim-stretch`` base image:

..  code-block:: Dockerfile

    FROM divio/base:0.4-py3.7-slim-stretch


..  important::

    If the relevant sections in the ``Dockerfile`` are surrounded by the Divio-specific comment tags::

        # <DOCKER_FROM>
        ...
        # </DOCKER_FROM>

    remove these tags - otherwise the Control Panel will simply overwrite your changes. See our :ref:`Dockerfile
    reference guide <dockerfile-reference-DOCKER-FROM-section>` for more information on the ``# <DOCKER_FROM>`` section.

Test the build locally with ``docker-compose build`` before pushing the change to the cloud.


Caveats
-------

Different base images may provide different packages and libraries. Our newer images tend to be
slimmer, in order to make builds faster and to use fewer resources, but may lack some software
that your application previously relied on.

For example, you may encounter a build error after adopting one of these images, such as:

..  code-block:: text

    ENOGIT git is not installed or not in the PATH

In other words, Git was available in the old image but not the new one, and is required to build
the project. In such a case, the missing libraries should be :ref:`installed into the image
manually <install-system-packages>`.
