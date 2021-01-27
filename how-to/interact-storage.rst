.. raw:: html

    <style>
        .highlight .upperrow .endpoint, .highlight .lowerrow .region {text-decoration: overline;}
        .highlight .lowerrow .endpoint, .highlight .upperrow .region {text-decoration: underline;}
        div[class^=highlight] .manual pre {color: gray;}
        .highlight .segment {font-weight: bold;}
        .highlight .key {color: maroon}
        .highlight .secret {color: navy}
        .highlight .bucketname {color: orange;}
        .highlight .region {color: green}
        .highlight .endpoint {color: brown}
        .highlight .code {font-style: italic}
    </style>


.. _interact-storage:

How to interact with your project's cloud media storage
=======================================================

..  seealso::

    :ref:`work-media-storage`.

Your cloud project's media file storage is provided as a service. The available storage depends on the Divio region
your project uses. Most projects use Amazon Web Services's S3 service, or another S3 provider. Others use Microsoft
Azure blob storage.

Locally, your projects store their media in the ``/data/media`` directory, which you can interact with directly. You
can :ref:`use the Divio CLI to push and pull media to the cloud <divio_tools_cloud_storage>` if required.

You can also interact directly with the cloud storage service using a suitable client if required, though this is
rarely necessary.

.. warning::

  Cloud file operations do not necessarily have the same behaviours you may be used to from other models.
  It's important that you know what you are doing and understand the consequences of any actions or commands.



Direct access to cloud storage
------------------------------

In each case, you need to obtain your storage credentials for an environment from its storage DSN variable, and use
those with a suitable client.


.. _storage_access_details:

Obtaining your cloud storage access credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the Divio CLI to obtain the storage DSN for the environment (``DEFAULT_STORAGE_DSN`` for the default storage), for
example:

..  code-block:: bash

    divio project env-vars -s test --all --get DEFAULT_STORAGE_DSN

or:

..  code-block:: bash

    divio project env-vars -s test --all --get DEFAULT_STORAGE_DSN --remote-id <site id>

See :ref:`how to read environment variables <reading-env-vars>`.

This value contains the details you will need to use with a file transfer client for access to the
storage bucket.


Install the client
~~~~~~~~~~~~~~~~~~~~~~

..  tab:: S3

    `AWS CLI documentation <http://docs.aws.amazon.com/cli/>`_ is Amazon's official S3 client.

    There are others clients suitable for connecting to S3 storage, including:

    * `S3cmd <https://s3tools.org/s3cmd>`_, an alternative command-line utility
    * `Transmit <https://www.panic.com/transmit>`_, a storage client for Macintosh
    * `Cyberduck <https://cyberduck.io>`_, a storage client for Macintosh and Windows

    It's beyond the scope of this documentation to discuss their usage. A brief example using the official
    AWS client is given here.


..  tab:: Azure blob storage

    This section makes use of the `MS Azure CLI <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli>`_, which
    you will need installed.


Parse the storage DSN
~~~~~~~~~~~~~~~~~~~~~~

..  tab:: S3

    The two examples below show which sections of the DSN correspond to different
    parameters, for the hosts ``s3.amazonaws.com`` and ``sos.exo.io``:

    .. raw:: html

        <div class="highlight-default notranslate">
        <div class="highlight manual">
        <pre><span class="upperrow">s3://<span class="segment key">AKAIIE7LUT6ODIJA</span>:<span class="segment secret">TZJYGCfUZheXG%2BwabbotgBs6d2lxZW06OIbD</span>@<span class="segment bucketname">example-test-68564d3f78d04c5f-8f20b19.aldryn-media.io</span>.<span class="segment endpoint">s3-<span class="segment region">eu-central-1</span>.amazonaws.com</span>/?domain=example-test-68564d3f78d04c5f-8f20b19.aldryn-media.io</span>
        <span class="code">           <span class="segment key">key</span>                        <span class="segment secret">secret</span>                                       <span class="segment bucketname">bucket name</span>                          <span class="segment region">region</span>     <span class="segment endpoint">endpoint</span></span>
        <span class="lowerrow">s3://<span class="segment key">EXO52e55b187195d</span>:<span class="segment secret">iITF12F1tim9zBxITexrvL_bAghgK_z4w1hEuu</span>@<span class="segment bucketname">example-test-765482644ac540dbb23367cf3837580b-f0596a8</span>.<span class="segment endpoint">sos-<span class="segment region">ch-dk-2</span>.exo.io</span>/?auth=s3</span></pre>
        </div>
        </div>

    The *secret* may contain some symbols encoded as hexadecimal values, and you will need to change
    them back before using them:

    * ``%2B`` must be changed to ``+``
    * ``%2F`` must be changed to ``/``

    For any other values beginning with ``%`` use `a conversion table
    <https://en.wikipedia.org/wiki/ASCII#Printable_characters>`_.

    The *bucket name* identifies the resource you wish to work with.

    .. _storage-region:

    The **region** is contained in the **endpoint**, the S3 host name. It may be implicit, as
    in the case of Amazon's default ``us-east-1``:

    +--------+---------------------------------+----------------+---------------------+
    |Provider| Endpoint                        |Region          |Location             |
    +========+=================================+================+=====================+
    |Amazon  |``s3.amazonaws.com``             |``us-east-1``   |US East (N. Virginia)|
    +        +---------------------------------+----------------+---------------------+
    |        |``s3-eu-central-1.amazonaws.com``|``eu-central-1``|EU (Frankfurt)       |
    +        +---------------------------------+----------------+---------------------+
    |        |``s3-eu-west-2.amazonaws.com``   |``eu-west-2``   |EU (London)          |
    +--------+---------------------------------+----------------+---------------------+
    |Exoscale|``sos-ch-dk-2.exo.io``           |``ch-dk-2``     |Switzerland          |
    +--------+---------------------------------+----------------+---------------------+

    See `Amazon's S3 regions table
    <http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region>`_ for more information about
    regions and their names.

    The *endpoint* is the address that the client will need to connect to.

..  tab:: Azure blob storage

    The examples below shows which sections of the DSN correspond to different
    parameters:

    ..  raw:: html

        <div class="highlight-default notranslate">
        <div class="highlight manual">
        <pre><span class="upperrow">az://<span class="segment key">exampletest43b4705bdf</span>:<span class="segment secret">c2U9MjAzNi0wMS0y</span>@<span class="segment bucketname">@blob.core.windows.net</span></span>
        <span class="code">         <span class="segment key">account name</span>       <span class="segment secret">encoded token</span>          <span class="segment bucketname">host name</span>                          <span class="segment region">region</span>     <span class="segment endpoint">endpoint</span></span>
        </div>
        </div>

    Note down the parameters ready for use.

    The encoded token needs to be `decoded from Base64 format <https://www.base64decode.org>`_; the decoded token will
    look something like::

        2036-01-22T08%3A56%3A16Z&sp=rwdlc&sv=2018-11-09&ss=b&srt=co&sig=ahD3gmIxymeattHsQ4mePWE5DFUol%2BW6byQt5EZ0H/U%3D

    Your media container is always named ``public-media`` by default.


Using the client
~~~~~~~~~~~~~~~~~~~~~~

..  tab:: S3

    Run::

        aws configure

    You will be prompted for some of the :ref:`storage access parameters <storage_access_details>`:

    * *AWS Access Key ID* - *key*
    * *AWS Secret Access Key* - *secret key*
    * *Default region name* - *storage region*

    The ``aws configure`` command stores the configuration in ``~/.aws``.


    Run ``aws s3`` followed by options, commands and parameters. For example, to list the contents of a
    bucket::

        ➜ aws s3 ls example-test-68564d3f78d0935f-8f20b19.aldryn-media.io
               PRE filer_public/
               PRE filer_public_thumbnails/


    Or, to copy (``cp``) a file from your own computer to S3::

        ➜ aws s3 cp example.png s3://example-test-68564d3f78d04c5f-8f20b19.aldryn-media.io/example.png
        upload: ./example.png to s3://example-test-68564d3f78d04c5f-8f20b19.aldryn-media.io/example.png

    ..  admonition:: Using AWS CLI with other providers

        For non-AWS providers, such as Exoscale, you will need to add the ``--url-endpoint`` option to
        the command, as the AWS CLI assumes an endpoint on ``.amazonaws.com/``. For the Exoscale
        example above, you would use::

            aws s3 --endpoint-url=https://sos-ch-dk-2.exo.io [...]

        Note that the scheme (typically ``https://``) must be included.


..  tab:: Azure blob storage

    Use the parameters with the Azure CLI, for example::

        az storage blob list --container-name public-media --account-name exampletest43b4705bdf --sas-token se="2036-01-22T08%3A56%3A16Z&sp=rwdlc&sv=2018-11-09&ss=b&srt=co&sig=ahD3gmIxymeattHsQ4mePWE5DFUol%2BW6byQt5EZ0H/U%3D"


.. _divio_tools_cloud_storage:

Use the Divio CLI for local access to Cloud storage
-----------------------------------------------------

The project's media files can be found in the ``/data/media`` directory, and
can be managed and manipulated in the normal way on your own computer.

Be aware that if you edit project files locally, your operating system may save
some hidden files. When you push your media to the cloud, these hidden files
will be pushed too. This will however not usually present a problem.


Pushing and pulling media files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`Divio CLI <divio-cli-command-ref>` includes ``pull`` and ``push`` commands that target the test or live server as
required.

..  warning::

    Note that all push and pull operations **completely replace** all files at
    the destination, and **do not perform any merges of assets**. Locally, the
    ``/data/media`` directory will be deleted and replaced; on the cloud, the
    entire bucket will be replaced.


Limitations
~~~~~~~~~~~

You may encounter some file transfer size limitations when pushing and pulling media using the Divio CLI. Interacting
directly with the storage service, as described above, is a way around this.

It can also be much faster, and allows selective changes to files in the system.


Configuring S3 buckets
----------------------

Storage ACLs (Access Control Lists)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When uploading files to your storage, you may need to specify the ACLs explicitly - in effect, the
file permissions - on the files. If you don't set the correct ACLs, you may find that attempts to
retrieve them (for example in a web browser) give an "access denied" error.

On AWS S3, the `public-read ACL
<https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ needs to be set
(by default it's `private`). This is the ACL required for general use.

For example, you can use ``--acl public-read`` as a flag for operations such as ``cp``, or ``aws
s3api put-object-acl`` and ``aws s3api get-object-acl`` to set set and get ACLs on existing objects.


.. _interact-storage-cors:

Enable CORS
~~~~~~~~~~~~~

CORS (cross-origin resource sharing) is a mechanism that allows resources on one domain to be
served when requested by a page on another domain.

These requests are blocked by default by S3 media storage; when a request is blocked, you'll see an error reported in the browser console:

..  code-block:: text

    Access to XMLHttpRequest at 'https://example.divio-media.com/images/image.jpg' from origin
    'https://example.us.aldryn.io' has been blocked by CORS policy: No
    'Access-Control-Allow-Origin' header is present on the requested resource.

In order to resolve this, the storage bucket needs to be configured to allow requests from a
different origin.

This can be done using the AWS CLI's S3 API tool (see above). Now you can check for any existing CORS configuration:

..  code-block:: bash

    aws s3api get-bucket-cors --bucket <bucket-name>

You will receive a ``The CORS configuration does not exist`` error if one is not yet present.

A CORS configuration is specified in JSON. It's beyond the scope of this documentation to outline
how your bucket should be configured for CORS; see AWS's own `Configuring and using cross-origin
resource sharing <https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html>`_ documentation
for more.

However an example that allows ``GET`` and ``HEAD`` requests from any origin would be:

..  code-block:: JSON

    {
       "CORSRules": [
           {
               "AllowedHeaders": ["*"],
               "AllowedMethods": ["GET", "HEAD"],
               "AllowedOrigins": ["*"],
               "MaxAgeSeconds": 3000
           }
       ]
    }

Save your configuration as a file (``cors.json``) and use the API to upload it to the bucket:

..  code-block:: bash

    aws s3api put-bucket-cors --bucket <bucket-name> --cors-configuration file://cors.json

See the `AWS S3 CLI API documentation
<https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/index.html#cli-aws-s3api>`_
for further information about available operations.

..  note::

    You may receive a ``GetBucketCors operation: Access Denied`` error when attempting to use the
    S3 API with some older buckets. If this occurs, but operations such as ``aws s3 ls`` work as
    expected, then your bucket will need to be updated. Please contact Divio support so that we can
    do this for you.
