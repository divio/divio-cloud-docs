..
  project-services-info
  Services view

.. raw:: html

    <style>
        table.docutils {text-align: center;}
        .new {border-radius: 100px; padding-left: 10px; padding-right: 10px; color: #fff; background-color: #0bf; font-size: 80%;}
        .prov {border-radius: 100px; padding-left: 10px; padding-right: 10px; color: #fff; background-color: #96b236; font-size: 80%;}
        .pending {border-radius: 100px; padding-left: 10px; padding-right: 10px; color: #fff; background-color: #ffa33d; font-size: 80%;}
        .deleted {border-radius: 100px; padding-left: 10px; padding-right: 10px; color: #fff; background-color: red; font-size: 80%;}
    </style>


.. _services:

Service management (Beta)
=========================

..  note::

    The Services view is currently provided as a Beta feature.

As well as its application code, a Divio project can include various services that are provided independently, such as a
database, media storage, a message queue and so on. These can be added, removed and configured in the *Services* view of any
project.


.. image:: /images/services.png
   :alt: 'Services'
   :class: 'main-visual'

Projects include a Postgres database and S3 media object storage by default; additional services such as alternative databases,
Elasticsearch and so on are also available.

See :ref:`Available services <available-services>` for an outline of services currently provided.

Multiple instances of a service - for example, two Postgres databases - may be used at the same time.


..
  project-services-install-service
  Add service dialog

.. _managing-services:

Service management via the Control Panel
-----------------------------------------

Before services can be configured for a project, the project's subscription must be updated to include them. For example, to
add Elasticsearch, you would add the requisite number of *Elasticsearch* instances via the *Subscription* view. Once added,
those services will be available to add in the *Services* view.


Adding and attaching
~~~~~~~~~~~~~~~~~~~~

Making a service available to an application is a two-stage process:

First, the service must be **added** to each environment that requires it. A unique prefix should be provided in case other
instances of the same service have already been applied.

Next, the environment must be deployed. Deployment **provisions** the service, and **attaches** it to the application.

If required, the option exists to provision a service independently of attachment. In this state, the application has not yet
been deployed with the environment variables it needs to use the service, but the service itself is functional and usable.
In the case of a media storage or database service, for example, this would allow you to populate it in advance of the
application's next deployment.


Detaching and removing
~~~~~~~~~~~~~~~~~~~~~~

A service may be **detached** if it is no longer to be used by the application. Like attachment, this requires a
deployment to take effect.

If a service is no longer required, it can be **removed**. An attached service will need to be *detached* before it can
be removed.

*Removing* a service is a *destructive operation*. It will permanently delete any data used by that service instance.

*Detaching* a service is *non-destructive*. However if the application depends on the service, detaching it may cause a
deployment or runtime error.

In the case of a deployment error following a detachment command, the service will not be detached, and the application
will continue running in its previous configuration. This safeguards a running application.


States
~~~~~~

Services will exist in a number of states across their lifetime:

.. role:: new
.. role:: pending
.. role:: deleted
.. role:: prov

+------------+----------------------+-----------------------------+----------------------+-------------------------------+---------------------+---------------------+
| :new:`new` | :prov:`provisioning` |:pending:`pending attachment`|  :new:`attached`     | :pending:`pending detachment` | :pending:`detached` | :deleted:`removed`  |
+------------+----------------------+-----------------------------+----------------------+-------------------------------+---------------------+---------------------+
| not functional                    | functional                  |        usable by the application                     | functional          | not functional      |
+------------+----------------------+-----------------------------+----------------------+-------------------------------+---------------------+---------------------+
