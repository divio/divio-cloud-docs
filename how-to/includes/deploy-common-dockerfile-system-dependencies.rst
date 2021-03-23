Install system-level dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Dockerfile`` needs to install any system dependencies required by the application. For example, if your chosen base image is Debian-based, you might run:

..  code-block:: Dockerfile

    RUN apt-get update && apt-get install -y <list of packages>
