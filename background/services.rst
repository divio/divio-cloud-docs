..  Do not change this document name
    Referred to by: tutorial message 142 project-services-info
    Where: in the Services view
    As: https://docs.divio.com/en/latest/background/services


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

As well as its application code, a Divio project can include various services that are provided independently, such as
a database, media storage, a message queue and so on. These can be added, removed and configured in the *Services* view
of any project.


.. image:: /images/services.png
   :alt: 'Services'
   :class: 'main-visual'

--------

Available services depend on the project's region. For example, S3 media storage is provided on AWS regions, and MS Blob storage on Azure regions.

See :ref:`Available services <available-services>` for an outline of services currently provided.

Multiple instances of a service - for example, two Postgres databases - may be used at the same time.


Environment variables
---------------------

For each environment, each service provisioned will create an environment variable, that can be used to configure
the applications that need to use it. Use the Divio CLI to obtain the values, for example:

..  code-block:: bash

    divio app env-vars --all

See :ref:`reading environment variables <reading-env-vars>` for more.


.. _managing-services:

Service management via the Control Panel
-----------------------------------------

Adding and attaching
~~~~~~~~~~~~~~~~~~~~

Making a service available to an application is a two-stage process:

First, the service must be **added** to each environment that requires it. A unique prefix should be provided in case
other instances of the same service have already been applied.

Next, the environment must be deployed. Deployment **provisions** the service, and **attaches** it to the application.

If required, the option exists to provision a service independently of attachment. In this state, the application has
not yet been deployed with the environment variables it needs to use the service, but the service itself is functional
and usable. In the case of a media storage or database service, for example, this would allow you to populate it in
advance of the application's next deployment.


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


.. _available-services:

Available services
------------------


.. _database:

Database
~~~~~~~~~

We provide Postgres and MySQL databases by default; other database systems can be provided on request.

Postgres is our database of choice, and configured by default with all projects.

Databases can use public (shared) or private clusters in the same region as the web application.


..  _media-storage:

Media object storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default file storage in Divio projects is handled by dedicated storage and hosting providers.

Depending on the project's region, these can be S3 providers such as `Amazon Web Services's S3 service
<https://aws.amazon.com/s3/>`_ or a generic S3 hosting service via another provider, or `MS Azure Blob storage <https://azure.microsoft.com/en-us/services/storage/blobs/>`_.

By default, media files are served by a Content Delivery Network in order to provide better performance.

..  seealso::

    * :ref:`work-media-storage`
    * :ref:`interact-storage`


.. _elasticsearch:

Elasticsearch
~~~~~~~~~~~~~~~~

Elasticsearch is provided as our default search engine, running on public (shared) or private clusters in the same region as
the web application. We support multiple versions of Elasticsearch.

.. _rabbitmq:

RabbitMQ
~~~~~~~~~

We provide RabbitMQ for messaging.
