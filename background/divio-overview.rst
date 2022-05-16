.. _divio-cloud-architecture:

Divio platform overview
=======================

Divio is a cloud management platform, providing Docker-based containerised web application hosting.

See :ref:`docker-basics` for an introduction to Docker and its key components.

Divio offers a local development environment that replicates almost
perfectly the Cloud environments in which applications run, eliminating many of
the pain-points of deployment caused by having to deal with different
environments in development and production.

In our architecture, we abstract functionality from configuration so that
functional components can be made immutable and stateless wherever possible.
This enables them to be replaced, added, moved and so on simply by spinning up
new instances, without requiring manual configuration.


.. _divio-cloud-infrastructure:

Cloud infrastructure
--------------------

Our cloud is vendor-neutral, and can be run on AWS, MS Azure and other infrastructures. Both our Control Panel and
customer applications can be deployed on public, private and on-premise infrastructures.

Our Control Panel and the cloud management architecture are built on a Python/Django stack. Our client sites run in
Docker containers. More information about our infrastructure can be provided on request.


Local development environment
--------------------------------

Thanks to Docker containerisation, we are able to provide :ref:`multiple environments for each application
<divio-project-environments>`, including a local development environment the replicates the application's cloud
environments.

Our toolchain helps set up the local environment, transfer data and media files to and from the cloud, and manage
deployments, from the command line.
