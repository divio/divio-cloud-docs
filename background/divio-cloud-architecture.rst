.. _divio-cloud-architecture:

The Divio Cloud architecture
============================


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
^^^^^^^^^^^^^^^^^^^^^^

Each Divio Cloud project includes three environments, each of which will create
a version of the website.

The three environments are created in Docker containers from the same images.

* *Local*, running on your own computer
* *Test*, running on our Cloud servers
* *Live*, running on our Cloud servers

In our workflow, development is done locally, before being deployed to *Test*
and finally to *Live*.


Project site stack
^^^^^^^^^^^^^^^^^^

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


.. _boilerplates_reference:

Boilerplates
^^^^^^^^^^^^

Divio Cloud projects represent web projects. Each project requires a frontend,
however minimal - at the very least, a basic ``base.html`` template. In order
to make Divio Cloud projects immediately useful, they each come with frontend
files included. These are defined by the site's :ref:`Boilerplate
<about-boilerplates>`, a set of default templates and static file.

Typically, a Boilerplate will define how the Django templates are structured and
make opinionated choices about what JavaScript frameworks and CSS tools are
used.

Various Boilerplates are provided as defaults, but it's also possible to define
and reuse your own.

Our simplest Boilerplates provide only basic HTML and CSS, but more
sophisticated ones include advanced frontend tooling: NPM, webpack, Sass and
other components.


Project repository branches
^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, each project's code is in its ``develop`` branch. This is then
pushed our Git server, where it can be deployed to the *Test* or *Live* servers
(our strongly -recommended workflow is always to deploy to *Test* first),

However, on request different branches can be set for the *Test* and *Live* servers - for example, ``develop`` and ``master`` respectively.

In this workflow you would work on ``develop`` before manually merging into
``master``, and then deploying *Live*.


Deployment
^^^^^^^^^^

A number of optimisations have been built into our Cloud deployment process to
make deployments faster and more reliable.

Python packaging
~~~~~~~~~~~~~~~~

We maintain our own Python Package Index, with which has pre-built
platform-specific `wheels <http://pythonwheels.com>`_ for all Python packages.

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
