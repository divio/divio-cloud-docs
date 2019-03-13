.. _divio-cloud-architecture:

Divio Cloud overview
====================


The Divio Cloud is a Docker-based platform-as-a-service. See
:ref:`docker-basics` for an introduction to Docker and its key components.

The Divio Cloud offers a local development environment that replicates almost
perfectly the Cloud environments in which applications run, eliminating many of
the pain-points of deployment caused by having to deal with different
environments in development and production.

In our architecture, we abstract functionality from configuration so that
functional components can be made immutable and stateless wherever possible.
This enables them to be replaced, added, moved and so on simply by spinning up
new instances, without requiring manual configuration.


.. _divio-cloud-infrastructure:

Divio Cloud infrastructure
--------------------------

Our Cloud is built on a Python/Django stack. Our client sites run in Docker
containers. More information about our infrastructure can be provided on
request.


.. _divio-cloud-projects:

Divio Cloud projects
--------------------

The three environments
~~~~~~~~~~~~~~~~~~~~~~

Each Divio Cloud project includes three environments, each of which will create
a version of the website.

The three environments are created in Docker containers from the same images.

* *Local*, running on your own computer
* *Test*, running on our Cloud servers
* *Live*, running on our Cloud servers

In our workflow, development is done locally, before being deployed to *Test*
and finally to *Live*.


.. _default-project-conditions:

Default project conditions
^^^^^^^^^^^^^^^^^^^^^^^^^^

Some of these conditions may be easily altered according your needs, for example the ``DEBUG``
setting. See also :ref:`local-in-live-mode`.

+----------------------------------+------------------+----------------------------+---------------------------+
|                                  | Local            | Test                       | Live                      |
+==================================+==================+============================+===========================+
| ``STAGE`` environment variable   | ``local``        | ``test``                   | ``live``                  |
+----------------------------------+------------------+----------------------------+---------------------------+
| ``DEBUG`` environment variable   | ``True``         |``True``                    | ``False``                 |
+----------------------------------+------------------+----------------------------+---------------------------+
| static files served by           | Python runserver |  uWSGI                                                 |
+----------------------------------+                  +----------------------------+---------------------------+
| media files served by            |                  | our Cloud S3 service                                   |
+----------------------------------+------------------+----------------------------+---------------------------+
| database runs in                 | a local container| our Cloud database cluster                             |
+----------------------------------+------------------+----------------------------+---------------------------+
| number of application containers | one                                           | according to subscription |
+----------------------------------+------------------+----------------------------+---------------------------+
| application container sleeps     | n/a              | after 15 minutes' activity | never                     |
+----------------------------------+------------------+----------------------------+---------------------------+


Project site stack
~~~~~~~~~~~~~~~~~~

The stack running Cloud sites is:

Container
    Docker
Operating system
    Ubuntu Linux
Web server/web application gateway
    Divio loadbalancer plus uWSGI (local sites use the Django runserver.)
Database
    Postgres (Test and Live sites use an AWS database; Local sites use a
    database running in another local container.)
Applications
    Python/Django


Docker on Divio Cloud
---------------------

A Divio Cloud project is defined by its *repository*. This contains the instructions required to
build it, such as source code for the project, a ``Dockerfile``, ``requirements.in`` and so on.

At deployment time, our infrastructure will typically build a new *image* based on those
instructions. It's important to note that the *same* instructions might produce a *different* image
- for example, if the instructions specify that Django should be installed, but do not specify
exactly which version of Django (say, ``django>=2.0``) then the package manager will install the
most recent version that matches. The same goes for Node dependencies and other items.

In some circumstances, the build process will *not* build a new image:

* If there are no new commits in the repository, and an image has been built already for the *Test*
  server, that image will be re-used for the *Live* server.
* When deploying a mirror project, the image already created for the original will be re-used.

A Docker *container* (an actual running instance) is then created from that image. The container
will use whatever environment variables are applied to that particular server, which could be the
local, Test or Live environment.

In other words, the repository is like the DNA that contains the instrutions for the building of a
living organism. In principle, every instance of that organism with the same DNA could be
identical, but any differences in environment - or environment variables - will also be reflected
in the actual organism - or site - that is created.


Docker layer caching
~~~~~~~~~~~~~~~~~~~~

We *don't* use Docker-level layer caching, as certain cases can produce
unexpected results:

* Unpinned installation commands might install cached versions of software,
  even where the user expects a newer version.
* Commands such as ``apt-get upgrade`` in a Dockerfile could similarly
  fail to pick up new changes.
* Our clustered setup means that builds take place on different hosts. As
  Docker layer caching is local to each host, this could mean that subsequent
  builds use different versions, depending on what is in each host's cache.
