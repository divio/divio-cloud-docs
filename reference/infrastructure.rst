How we use terms
==============================

In any product, technical terms that have a generally-understood meaning in a wider context often refer more
specifically to some particular thing or implementation of it in the product - Divio is no exception. This guide is
intended to help make it clearer what we mean when we use certain terms.


Applications
------------

A Divio **application** is a collection of orchestrated services, managed all together in one place in our Control Panel. In general, Divio billing is based on application subscriptions.


Regions
--------

We provide multiple **regions** for application deployment. For example, if you deploy an application using our free
Developer plan, it will use our North America public region, which runs on Amazon Web Services.

A Divio region is the infrastructure required to run our services, at a physical location somewhere in the world.

As well as having a physical location, each region uses resources belonging to a specific vendor or provider, which 
could be Amazon Web Services, MS Azure, another cloud provider, or even a customer's own resources.

Finally, for any physical region, we may have multiple logical regions. For example, we can provide a customer with
a dedicated, isolated region of their own, that's based in the same physical region as one of our public regions.

Divio applications and their services can be migrated from one region to another.


Services
--------

For each region, we provide various **services** - application runners, databases, media storage, and so on - that a
complete web application requires in order to run.

Self-service applications on Divio use services on our public regions by default. However as well as entire dedicated
regions, it's also possible to have individual dedicated services (for example, a database) according to needs.


Divio components
----------------

Control Panel
~~~~~~~~~~~~~

A web-based frontend for managing Divio applications.


Application builders
~~~~~~~~~~~~~~~~~~~~

Our application builders build Docker images from an application's codebase.


Application controllers
~~~~~~~~~~~~~~~~~~~~~~~

A region's application controllers deploy and scale applications, launching containers from images that have been built
and putting them into production.


Application runners
~~~~~~~~~~~~~~~~~~~

An application runner is a virtual server that hosts containers for one or more applications, and looks after them
while they are running.


Ingress controllers
~~~~~~~~~~~~~~~~~~~

Our ingress controllers are sometimes referred to as load-balancers. They are close to the edge of our infrastructure,
and hand off incoming traffic to applications' containers.

