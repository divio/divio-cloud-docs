.. _dockerfile-reference:

The ``Dockerfile``
==================

`Divio <https://www.divio.com>`_ uses dockerized applications. Each :ref:`Docker image <image-reference>` is defined by 
a ``Dockerfile``, that describes what is in the image and how :ref:`containers <container-reference>` created from it 
should be built.

The Dockerfile is simply a text document, containing all the commands that would be issued on the
command-line to build an image - in short, the ``Dockerfile`` defines an environment.

The Dockerfile is built automatically, and populated with appropriate commands (see below).
However, you can also add any commands you wish to the ``Dockerfile``, for example to :ref:`install
system packages <install-system-packages>`, or to configure the environment.

..  important::

    The ``Dockerfile`` executes its commands in sequence. This means that commands to install Node
    (for example) must come before commands to run Node packages.





