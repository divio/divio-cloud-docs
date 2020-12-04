.. _manage-base-image:

How to manage a project's base image
=========================================================

The base image of your project is determined by its ``Dockerfile``.

Whatever base image is used in a project should include the runtime environment(s) you need for your application, such
as an appropriate version of Python.


Specify the base image in the ``Dockerfile``
--------------------------------------------

For example, to use Divio's own ``0.4-py3.7-slim-stretch`` base image:

..  code-block:: Dockerfile

    FROM divio/base:0.4-py3.7-slim-stretch

Or to use the official Python 3.9 image from Docker:

..  code-block:: Dockerfile

    FROM python:3.9.0


.. _manage-base-image-choosing:

Choosing an appropriate base image
----------------------------------

Pin images to a particular version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is always wise to pin a base image to a particular version number. For example, ``FROM python`` doesn't specify
which version of Python will be installed, and a future update could introduce breaking changes. Specify the version,
e.g. ``FROM python:3.9.0``, to prevent this from happening.

Note also that the underlying operating system components could change. Choosing ``python:3.9.0`` on a Linux-based
architecture such as Divio's will use Debian as the basis for the operating system components, but will not specify
which version of Debian. Pinning it further with for example ``python:3.9.0-buster`` may be a good idea.

When you pin versions, you should periodically check that the version you have chosen is still well-supported,
particularly for security updates.


Check included components
~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple different tagged versions can be provided for the same fundamental image. For example, for the `official
Python image <https://hub.docker.com/_/python/>`_:

* ``python:3.9.0``
* ``python:3.9.0-buster``
* ``python:3.9.0-slim-buster``
* ``python:3.9.0-alpine3.12``

The ``slim-buster`` and ``alpine`` variants might seem attractive, because they are lightweight. Be aware however that
if as a result they lack components that you must instead install manually, you may lose much of the benefit. For
example, ``python:3.9.0-slim-buster`` does not include binaries for Postgres or MySQL; if you need them, which is
likely, ``python:3.9.0-buster`` would be a better choice.


Base images provided by Divio
---------------------------------

As well as the many images, official and unofficial, that are available and suitable for a vast variety of web
applications, we also provide a number of `Divio-optimised Docker base images for projects
<https://hub.docker.com/r/divio/base/tags>`_.

These base images provide an underlying Linux operating system layer, and other layers in the stack, upon which you can
build your custom application. For example, our Python base images will include a particular version of Python, and any
system-level components required to run it.


Divio-managed base image updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some projects include a ``Dockerfile`` that can be updated by the Divio Control Panel when updates are
available, and will contain lines such as:

..  code-block:: Dockerfile

    # <DOCKER_FROM>
    FROM divio/base:4.18-py3.6-slim-stretch
    # </DOCKER_FROM>

When new base images will be released with updates (for example, for newer Python releases) and other improvements or
changes, the Control Panel will indicate that updates are available in *Settings* > *Base Project*.

Note however that because the base image can also be specified in the repository via the ``Dockerfile``, the manual
setting will override what's indicated in the Dashboard.
