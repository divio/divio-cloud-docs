Elasticsearch instances
=======================

We currently provide multiple versions of Elasticsearch on different regions. Please contact 
`Divio <https://www.divio.com>`_ `support <https://www.divio.com/support/>`_ for more information_support if you need 
to specify a particular version for your application.


Access credentials
------------------------

When an Elasticsearch instance is added to an application, each environments will be provided with a
``DEFAULT_HAYSTACK_URL`` variable.

This variable contains the details required to access the instance, in the form::

    es+https+aws://<access key>:<secret key>@<host>/<index>-*

Your application will need to parse this URL appropriately. Note that the secret key may contain encoded characters that
need to be decoded.


Access limitations
------------------

Except for applications using a dedicated Elasticsearch instance, applications use one of our shared Elasticsearch 
clusters.

The connection URL we provide grants access *only* to a specific index, and not to other indexes. An application
may use only URLs that start with the index prefix we provided.

The reason for this limitation is that `the AWS ES permissions model could otherwise allow aliases to bypass intended
access restrictions
<https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-ac.html#es-ac-advanced>`_.
