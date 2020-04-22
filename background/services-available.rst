.. _available-services:

Available services
==================

..  seealso::

    :ref:`services`


.. _database:

Database
--------

We provide Postgres and MySQL databases by default; other database systems can be provided on request.

Postgres is our database of choice, and configured by default with all projects.

Databases can use public (shared) or private clusters in the same region as the web application.


..  _media-storage:

Media object storage
------------------------

Default file storage in Divio Cloud projects is handled by dedicated storage and hosting providers.

Depending on the project's region, these can be S3 providers such as `Amazon Web Services's S3 service
<https://aws.amazon.com/s3/>`_ or a generic S3 hosting service via another provider, or `MS Azure Blob storage <https://azure.microsoft.com/en-us/services/storage/blobs/>`_.

By default, media files are served by a Content Delivery Network in order to provide better performance.

..  seealso::

    * :ref:`work-media-storage`
    * :ref:`interact-storage`


.. _elasticsearch:

Elasticsearch
----------------

Elasticsearch is provided as our default search engine, running on public (shared) or private clusters in the same region as
the web application. We support multiple versions of Elasticsearch.

.. _rabbitmq:

RabbitMQ
---------

We provide RabbitMQ for messaging.
