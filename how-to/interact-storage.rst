.. _interact-storage:

How to interact with your project's media storage
=================================================

..  note::

    See also :ref:`work-media-storage`.

Your cloud project's media file storage is held on `Amazon Web Services's S3
service <https://aws.amazon.com/s3/>`_, or a generic S3 hosting service via
another provider. Currently, most projects use Amazon's own S3 service, with
the exception of projects in our Swiss region.

Locally, your projects store their media in the ``/data/media`` directory.


.. _interact-storage-s3:

Direct access to your project's S3 storage
------------------------------------------

Occasionally you may need direct access to the S3 storage bucket for your
project. You can manage this using a client of your choice that supports S3 and
the particular storage provider.

..  warning::

    You make use of this access at your own risk.

    S3 file operations tend to be **destructive** and do not necessarily have
    the same behaviours you may be used to from other models, such as FTP. Make
    sure that you know what you are doing and that you understand the
    consequences of any actions or commands.

    For example, note that all push and pull operations **completely replace**
    all files at the destination, and **do not perform any merges of assets**.
    Locally, the ``/data/media`` directory will be deleted and replaced; on the
    cloud, the entire bucket will be replaced.


.. _storage_access_details:

Obtain your storage access details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Control Panel for your project, visit the ``/doctor`` URL. For each of
the Test and Live servers, you'll see a ``DEFAULT_STORAGE_DSN`` value listed,
for example:

.. image:: /images/default-storage-dsn.png
   :alt: 'Default storage DSN value'

This value contains the details you will need to use with a file transfer
client for access to the storage bucket.


.. _aws_example:

Amazon Web Services example
^^^^^^^^^^^^^^^^^^^^^^^^^^^

===============  =============================================================
Parameter        Value
===============  =============================================================
**DSN value**    ``s3://AKAIIEJALP7LUT6ODIJA:TZJYGCfUZheXG%2BwANMFabbotgBs6d2lxZW06OIbD@example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io.s3.amazonaws.com/?domain=example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io``
**key**          ``AKAIIEJALP7LUT6ODIJA``
**secret**       ``TZJYGCfUZheXG+wANMFabbotgBs6d2lxZW06OIbD`` (see :ref:`DSN-reserved-characters`)
**bucket name**  ``example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io`` (from ``?domain=`` query)
**S3 host**      ``s3.amazonaws.com``
**AWS region**   ``us-east-1``
**Served at**    ``example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io`` (from ``?domain=`` query)
===============  =============================================================


AWS regions
...........

The region domain name in the example above is ``s3.amazonaws.com``, so the
Region name is ``us-east-1``, the default AWS region

``us-east-1`` applies when no other region name is explicitly given. Other
regions will be identified in the ``s3.amazonaws.com`` portion of the URL. For
example, storage on our EU region would refer to
``s3-eu-central-1.amazonaws.com``.

See the `AWS S3 regions table
<http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region>`_ for more
information about regions and their names.


.. _DSN-reserved-characters:

Reserved characters
...................

In the secret in the AWS URL, certain reserved symbols (``+``, ``-``, ``=``,
``.``, ``_``, ``:``, ``/``) will be encoded as hexadecimal values. You will
need to convert these back to use them in your client. For example, ``%2B``
will become ``+``, ``%2F`` will become ``/`` and so on. Use `a conversion table
<https://en.wikipedia.org/wiki/ASCII#Printable_characters>`_ for any other
values beginning with ``%``.


Exoscale (Divio Cloud Swiss region) example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

===============  =============================================================
Parameter        Value
===============  =============================================================
**DSN value**    ``s3://EXO52e55eb39187195ffdd72219:iITF12F1t123tim9zBxITexrvL_bAghgK_z4w1hEuu00@example-test-765482644ac540dbb23367cf3837580b-f0596a8.sos.exo.io/?auth=s3``
**key**          ``EXO52e55eb39187195ffdd72219``
**secret**       ``iITF12F1t123tim9zBxITexrvL_bAghgK_z4w1hEuu00``
**bucket name**  ``example-test-765482644ac540dbb23367cf3837580b-f0596a8``
**S3 host**      ``sos.exo.io``
===============  =============================================================


S3 clients
----------

A number of CLI and GUI S3 clients are available. Information is provided here
for a few of them.


AWS CLI
~~~~~~~

Amazon's official S3 client. `AWS CLI documentation
<http://docs.aws.amazon.com/cli/>`_. Supports AWS only, not other providers.

It's beyond the scope of this document to provide comprehensive guidance on
using the AWS CLI, but the steps below should get you started.


Install AWS CLI
^^^^^^^^^^^^^^^

Install with ``pip install awscli`` (it's a Python application).


Configure the client for your project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run ``aws configure``, and you will be prompted for the *AWS Access Key ID*,
*AWS Secret Access Key* and *Default region name*, which you can extract from
the :ref:`DEFAULT_STORAGE_DSN <storage_access_details>` - see
:ref:`aws_example`, above - and *Default output format*.


Interact with your storage
^^^^^^^^^^^^^^^^^^^^^^^^^^

Run ``aws s3`` followed by a command and options.

For example, to list the contexts of a bucket::

    ➜ aws s3 ls example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io
           PRE filer_public/
           PRE filer_public_thumbnails/

or to copy (``cp``) a file from your own computer to S3::

    ➜ aws s3 cp example.png s3://example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io/example.png
    upload: ./example.png to s3://example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io/example.png

Run ``aws s3 help`` for more information on commands, or refer to the `AWS CLI
Command Reference
<http://docs.aws.amazon.com/cli/latest/reference/s3/index.html>`_


Transmit
~~~~~~~~

`Transmit file transfer application for Macintosh
<https://www.panic.com/transmit>`_.

Create a new connection with the following settings:

=============  ===============
Setting        Value
=============  ===============
Protocol       *Amazon S3*
Address        S3 host name from DSN value
Access Key ID  key from DSN value
SECRET         secret from DSN value
Remote Path    bucket name from DSN value
=============  ===============


Cyberduck
~~~~~~~~~

`Cyberduck <https://cyberduck.io>`_, an open-source client for Macintosh and
Windows.

Note that because the connection requires you to provide details of the bucket,
you must start by creating a new bookmark, as the *Open Connection* dialog in
Cyberduck doesn't provide this as an option.

For Exoscale (Divio Cloud Swiss region) deployments, you will need to download
and install the `Exoscale profile for Cyberduck
<https://svn.cyberduck.io/trunk/profiles/exoscale.cyberduckprofile>`_.

Connection settings:

========================  ====================  =============================
Setting                   Value
------------------------  ---------------------------------------------------
\                         AWS                   Exoscale
========================  ====================  =============================
Connection type           *Amazon S3*           *exoscale Swiss Object Store*
Address                   ``s3.amazonaws.com``  ``sos.exo.io``
Access Key ID/API Key     key from DSN value
------------------------  ---------------------------------------------------
Path                      bucket name from DSN value
------------------------  ---------------------------------------------------
Secret Access/Secret Key  secret from DSN value
------------------------  ---------------------------------------------------
========================  ====================  =============================

s3cmd
~~~~~~~~~

`s3cmd <http://s3tools.org/s3cmd>`_ is a command-line utility that supports
both AWS and other providers, like Exoscale

s3cmd requires a configuration file, which can either be ``~/.s3cfg``, or a
location passed in by the ``-c`` flag. 

For Exoscale, the following configurations should be used: 


========================  ====================
Setting                   Value
========================  ====================
host_base                 sos.exo.io
host_bucket               bucket_name.sos.exo.io
access_key                (key)
secret_key                (secret)
use_https                 True
========================  ====================

The result is a ``.s3cfg`` configuration file in the following format::

    [default]
    host_base = sos.exo.io
    host_bucket = example-test-68564d3f78d04cd2935f-8f20b19.sos.exo.io
    access_key = EXOaaaaaaaaaaaaaaaaaaaaaaaa
    secret_key = bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
    use_https = True

Then, to invoke `s3cmd commands <http://s3tools.org/usage>`_ such as ``ls``::

    ➜ s3cmd ls s3://example-test-68564d3f78d04cd2935f-8f20b19/ --signature-v2
             DIR s3://example-test-68564d3f78d04cd2935f-8f20b19/filter_public_thumbnails
             DIR s3://example-test-68564d3f78d04cd2935f-8f20b19/filter_public/

The flag ``--signature-v2`` must be used to ensure the authentication details are accurate for Exoscale


Access to storage when running locally
--------------------------------------

The project's media files can be found in the ``/data/media`` directory, and
can be managed and manipulated in the normal way on your own computer.

Be aware that if you edit project files locally, your operating system may save
some hidden files. When you push your media to the cloud, these hidden files
will be pushed too. This will however not usually present a problem.


Pushing and pulling media files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`Divio app <divio-app>` includes an option to **Upload** (push) and
**Download** (pull) media files to and from the cloud test server.

The :ref:`Divio CLI <divio-cli-ref>` includes :ref:`pull <divio-project-pull>`
and :ref:`push <divio-project-push>` commands that target the test or live
server as required.

..  warning::

    Note that all push and pull operations **completely replace** all files at
    the destination, and **do not perform any merges of assets**. Locally, the
    ``/data/media`` directory will be deleted and replaced; on the cloud, the
    entire bucket will be replaced.


Limitations
~~~~~~~~~~~

You may encounter some file transfer size limitations when pushing and pulling
media using the Divio app or the Divio CLI. :ref:`Interacting directly with the
S3 storage bucket <interact-storage-s3>` is a way around this.

It can also be much faster, and allows selective changes to files in the system.
