.. _docker-basics:

Docker basics
=============

`Docker <https://docker.com>`_ is a **containerisation** system.
Containerisation is also known as `operating-system-level virtualisation
<https://en.wikipedia.org/wiki/Operating-system-level_virtualization>`_. It
allows multiple independent containers to run on a single host. The containers
are isolated from each other and from the host.

Resource isolation features make it possible for the containers to share
underlying operating system resources. Whereas more traditional virtual
machines replicate an entire operating system, containerisation can provide a
much more lightweight solution to virtualisation, containing only the specific
stack layers required for a particular application.

Docker containers are thus smaller and consume fewer resources, avoiding the
memory and CPU overheads of full virtualisation. They are faster to start up,
manage and scale, and easier to move, around than full virtual machines.


Docker on Macintosh and Windows
-------------------------------

Docker requires a Linux host for its containers. On Linux systems, containers
will simply use the Linux operating system's resources. Macintosh and Windows
need to run a single Linux virtual machine to serve as the host.

This can be done in two ways:

* On **newer systems**, the `Alpine Linux <https://www.alpinelinux.org>`_ host
  is provided through native operating system virtualisation.

  (On Macintosh, it's provided by through *HyperKit*, a lightweight
  virtualisation system built on top of the *Hypervisor.framework* (macOS
  10.10 Yosemite and higher).

  On Windows, it's provided through a similar system, Microsoft's *Hyper-V*
  (Windows 10 Professional, Enterprise and Education editions).)

* On **older systems**, it requires a Linux virtual machine running in `VirtualBox
  <https://virtualbox.org>`_. This is managed by a tool called *Docker Toolbox*.


Key components
--------------

The two key components in Docker are:

* *Docker Engine*, the underlying daemon running on the host. Docker Engine is
  also confusingly sometimes referred to simply as *Docker* (to make things
  worse, there is also a command-line tool named ``docker``).
* *Docker Compose* (invoked as ``docker-compose``) is a tool for defining and
  managing multi-container applications; Divio projects use Docker Compose only
  in the local environment.


Glossary
--------

.. _application-reference:

Application
    Docker terminology uses "application" in much the same way that Django uses
    "project", a collection of components that together form a complete and
    self-contained system.

    In our case, a Docker application is the collection of components that is
    responsible for a website and its functionality, including everything from
    the database to the frontend code.

    A Docker application will typically include multiple *containers*.

.. _container-reference:

Container
    A Docker container is virtualised application environment. Unlike a virtual
    server, it doesn't need to provide every layer in a full working system.
    Instead, it encapsulates only the layers required to run an application.

.. _image-reference:

Image
    An image is a template. Each container is based on an image. Once an image
    has been created, each container created from it will provide exactly the
    same environment, and the applications in it will behave identically. An
    image is defined by its :ref:`Dockerfile <dockerfile-reference>`.

