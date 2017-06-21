.. _divio-cloud-architecture:

The Divio Cloud architecture
============================

..  todo::

    Decide what material in this section needs to be removed to `internal
    documentation
    <https://divio-ch.atlassian.net/wiki/display/TC/Divio+Cloud+-+general+descri
    ption+and+policies+for+clients>`_ only and what should be published by
    default.

The Divio Cloud is a Docker-based platform-as-a-service. See
:ref:`docker-basics` for an introduction to Docker and its key components.

The Divio Cloud offers a local development environment that replicates almosts
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

Servers
^^^^^^^

Our servers run Ubuntu 16.04.2 LTS, the latest officially-released AMI (Amazon Machine Image). They are cycled (replaced) regularly and frequently.

Patches can also be applied manually when required.

Application hosts
^^^^^^^^^^^^^^^^^

* Replacement frequency: typically one to four weeks
* Time to replace: five to ten hours

Load balancer hosts
^^^^^^^^^^^^^^^^^^^

* Replacement frequency: typically six weeks
* Time to replace: fifteen minutes

Database
^^^^^^^^

Postgres, on Amazon Web Services.

Storage
^^^^^^^

Amazon S3.

Containerisation
^^^^^^^^^^^^^^^^

Where possible, Docker containers in the Divio Cloud architecture provide
*functionality* (such as running an application) but do not maintain
*state*.

In general, state is maintained separately:

* configuration is maintained in enviroment settings
* database storage is handled by external database services
* file storage is handled by external storage services


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
files included. These are defined by the site's *Boilerplate*, a set of default
templates and static file.

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
``master``, and theb deploying *Live*.
