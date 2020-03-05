.. _manage-base-image:

How to change Python versions by changing the base image
=========================================================

..  seealso::

   Reference in :ref:`dockerfile-reference-DOCKER-FROM-section`


All Divio Cloud projects are based on a customised Docker image, which uses a version of Ubuntu Linux.

If you wish to change the Python version of your project, you will need to select a different base image in the project's ``Dockerfile``.

Our base images are published at `Divio base <https://hub.docker.com/r/divio/base/tags>`.

For example, if you wish to change to Python 3.7, you could use our 0.4-py3.7-slim-stretch base image by specifying it in the ``Dockerfile`` 
inside the ``<DOCKER_FROM>`` section as shown below:

..  code-block:: Dockerfile
    :emphasize-lines: 2

    # <DOCKER_FROM>
    FROM divio/base:0.4-py3.7-slim-stretch
    # </DOCKER_FROM>

Note that this should be tested locally with ``docker-compose build`` before being pushed to the cloud.
