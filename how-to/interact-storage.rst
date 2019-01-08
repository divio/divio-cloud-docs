.. raw:: html

    <style>
        .highlight .upperrow .endpoint, .highlight .lowerrow .region {text-decoration: overline;}
        .highlight .lowerrow .endpoint, .highlight .upperrow .region {text-decoration: underline;}
        div[class^=highlight] .manual pre {color: gray;}
        .highlight .segment {font-weight: bold;}
        .highlight .key {color: maroon}
        .highlight .secret {color: navy}
        .highlight .bucketname {color: olive}
        .highlight .region {color: green}
        .highlight .endpoint {color: brown}
        .highlight .code {font-style: italic}
    </style>


.. _interact-storage:

How to interact with your project's media storage
=================================================

..  seealso::

    :ref:`work-media-storage`.

Your cloud project's media file storage is held on an S3 service - typically `Amazon Web Services's
S3 service <https://aws.amazon.com/s3/>`_, or another S3 provider. Currently, most projects use
Amazon's own S3 service, or Exoscale for projects in our Swiss region.

Locally, your projects store their media in the ``/data/media`` directory, and you can interact
with those directly. Then, you can :ref:`use the Divio tools to push and pull media to the Cloud
<divio_tools_cloud_storage>` if required.

Occasionally you may need direct access to the S3 storage bucket for your
project. You can manage this using a client of your choice that supports S3 and
the particular storage provider.


.. _interact-storage-s3:

Interact with your project's Cloud S3 storage
----------------------------------------------

.. warning::

  Note that S3 file operations tend to be **destructive** and do not necessarily have the same
  behaviours you may be used to from other models, such as FTP. It's important that you know what
  you are doing and understand the consequences of any actions or commands.


.. _storage_access_details:

Obtain your storage access details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Control Panel for your project, visit the ``/doctor`` URL. For each of the Test and Live
servers, you'll see a ``DEFAULT_STORAGE_DSN`` value listed, for example:

.. image:: /images/default-storage-dsn.png
   :alt: 'Default storage DSN value'

This value contains the details you will need to use with a file transfer client for access to the
storage bucket. The two examples below show which sections of the DSN correspond to the different
parameters, for the hosts ``s3.amazonaws.com`` and ``sos.exo.io``:

.. raw:: html

    <div class="highlight-default notranslate">
    <div class="highlight manual">
    <pre><span class="upperrow">s3://<span class="segment key">AKAIIEJALP7LUT6ODIJA</span>:<span class="segment secret">TZJYGCfUZheXG%2BwANMFabbotgBs6d2lxZW06OIbD</span>@<span class="segment bucketname">example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io</span>.<span class="segment endpoint">s3-<span class="segment region">eu-central-1</span>.amazonaws.com</span>/?domain=example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io</span>
    <span class="code">              <span class="segment key">key</span>                            <span class="segment secret">secret</span>                                             <span class="segment bucketname">bucket name</span>                          <span class="segment region">region</span>       <span class="segment endpoint">endpoint</span></span>
    <span class="lowerrow">s3://<span class="segment key">EXO52e55beb39187195ddff72219</span>:<span class="segment secret">iITF12F1t321tim9zBxITexrvL_bAghgK_z4w1hEuu00</span>@<span class="segment bucketname">example-test-765482644ac540dbb23367cf3837580b-f0596a8</span>.<span class="segment endpoint">sos-<span class="segment region">ch-dk-2</span>.exo.io</span>/?auth=s3</span></pre>
    </div>
    </div>

The **key** identifies you as a user.

The **secret** may contain some symbols encoded as hexadecimal values, and you will need to change
them back before using them:

* ``%2B`` must be changed to ``+``
* ``%2F`` must be changed to ``/``

For any other values beginning with ``%`` use `a conversion table
<https://en.wikipedia.org/wiki/ASCII#Printable_characters>`_.

The **bucket name** identifies the resource you wish to work with.

.. _storage-region:

The **region** is contained in the **endpoint**, the S3 host name. Sometimes it may be implicit, as
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

The **endpoint** is the address that the client will need to connect to.


.. _save-aws-parameters:

Save the parameters
~~~~~~~~~~~~~~~~~~~

Copy and paste each of these parameters into a text file, so you have them ready for use. Now that
you have obtained the connection parameters, you can use them to connect with the client of your
choice.


Choose a client
~~~~~~~~~~~~~~~

How-to guides are provided below for connecting to our storage using:

* :ref:`AWS CLI <connect-aws-cli>`, Amazon's official S3 client
* :ref:`s3cmd <connect-s3cmd>`, an alternative command-line utility
* :ref:`Transmit <connect-transmit>`, a popular storage client for Macintosh
* :ref:`CyberDuck <connect-cyberduck>`, a popular storage client for Macintosh and Windows


.. _connect-aws-cli:

Connect using AWS CLI
~~~~~~~~~~~~~~~~~~~~~

`AWS CLI documentation <http://docs.aws.amazon.com/cli/>`_ is Amazon's official S3 client. It's a
free, Python-based application.


Install and configure AWS CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run::

    pip install awscli
    aws configure

You will be prompted for some of the :ref:`storage access parameters <storage_access_details>`
values, extracted from the DSN, that :ref:`you copied earlier <save-aws-parameters>`.

* *AWS Access Key ID* - *key*
* *AWS Secret Access Key* - *secret key*
* *Default region name* - *storage region*
* *Default output format* - leave blank


Interact with your storage
^^^^^^^^^^^^^^^^^^^^^^^^^^

Run ``aws s3`` followed by options, commands and parameters. For example, to list the contents of a
bucket::

    ➜ aws s3 ls example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io
           PRE filer_public/
           PRE filer_public_thumbnails/


Or, to copy (``cp``) a file from your own computer to S3::

    ➜ aws s3 cp example.png s3://example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io/example.png
    upload: ./example.png to s3://example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io/example.png

..  admonition:: Using AWS CLI with other providers

    For non-AWS providers, such as Exoscale, you will need to add the ``--url-endpoint`` option to
    the command, as the AWS CLI assumes an endpoint on ``.amazonaws.com/``. For the Exoscale
    example above, you would use::

        aws s3 --endpoint-url=https://sos-ch-dk-2.exo.io [...]

    Note that the scheme (typically ``https://``) must be included.

Additional usage information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run ``aws s3 help`` for more information on commands, or refer to the `AWS CLI Command Reference
<http://docs.aws.amazon.com/cli/latest/reference/s3/index.html>`_. The AWS CLI can maintain
multiple profiles and offers other features but it's beyond the scope of this documentation to
explain that here.

The ``aws configure`` command stores the configuration in ``~/.aws``.


.. _connect-s3cmd:

Connect using s3cmd
~~~~~~~~~~~~~~~~~~~

`S3cmd <https://s3tools.org/s3cmd>`_ is a free Python-based command line tool and client for
uploading, retrieving and managing data in Amazon S3 and other cloud storage service providers that
use the S3 protocol.


Install and configure s3cmd
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run::

    pip install s3cmd
    s3cmd --configure

You will be prompted for some of the :ref:`storage access parameters <storage_access_details>`
values, extracted from the DSN, that :ref:`you copied earlier <save-aws-parameters>`:

* *Access Key* - enter the *key* from the DSN
* *Secret Key* - enter the *secret key* from the DSN
* *Default Region* - enter the :ref:`storage region <storage-region>`
* *S3 Endoint* - enter the *endpoint* from the DSN

All other settings can be left untouched.

When you have entered the values, s3cmd will offer to test a connection with them (note that when
using AWS, this will **fail** - ignore this).


Interact with your storage
^^^^^^^^^^^^^^^^^^^^^^^^^^

Run ``s3cmd`` followed by options, commands and parameters. For example, to list the contents of a
bucket::

    s3cmd ls s3://example-test-68564d3f78d04cd2935f-8f20b19.aldryn-media.io

Note that the scheme (``s3://``) is required in front of the bucket name.


Additional usage information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run ``s3cmd`` for more information on commands, or refer to `Usage <https://s3tools.org/usage>`_.

Using ``s3cmd`` you can take advantage of ``--recursive`` properties for iterating over the entire
bucket contents; however it's beyond the scope of this documentation to explain this or other
features here.

``s3cmd --configure`` creates a configuration file at ``~/.s3cfg``.


.. _connect-transmit:

Connect using Transmit
~~~~~~~~~~~~~~~~~~~~~~

Install the `Transmit file transfer application for Macintosh <https://www.panic.com/transmit>`_.

Create a new connection. You will need to enter some of the :ref:`storage access parameters
<storage_access_details>` values, extracted from the DSN, that :ref:`you copied earlier
<save-aws-parameters>`:


=============  ===============
Setting        Value
=============  ===============
Protocol       *Amazon S3*
Address        *endpoint*
Access Key ID  *key*
Password       *secret key*
Remote Path    *bucket name*
=============  ===============


.. _connect-cyberduck:

Cyberduck
~~~~~~~~~

Install `Cyberduck <https://cyberduck.io>`_.

Create a new bookmark (note that you **cannot** simply use the *Open Connection* dialog, because
this will not allow you to provide the required bucket name in order to proceed). You will be
prompted for some of the :ref:`storage access parameters <storage_access_details>` values,
extracted from the DSN, that :ref:`you copied earlier <save-aws-parameters>`:

========================  ===============
Setting                   Value
========================  ===============
Protocol                  *Amazon S3*
Server                    *endpoint*
Access Key ID             *key*
Path (in *More Options*)  *bucket name*
========================  ===============

On attempting to connect, you will be prompted for the Secret Access Key; use the *secret key*.

For Exoscale (Divio Cloud Swiss region) deployments, you can also download and install the
`Exoscale profile for Cyberduck
<https://svn.cyberduck.io/trunk/profiles/exoscale.cyberduckprofile>`_, which includes some
prepared configuration.


.. _divio_tools_cloud_storage:

Use Divio tools for local access to Cloud storage
-----------------------------------------------------

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


Storage ACLs (Access Control Lists)
-----------------------------------

When uploading files to your storage, note that you may need to specify
explicitly the ACLs - in effect, the file permissions - on the files. If you
don't set the correct ACLs, you may find that attempts to retrieve them (for
example in a web browser) give an "access denied" error.

On AWS S3, the `public-read ACL
<https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ needs to be set
(by default it's `private`). This is the ACL required for general use.

For example, you can use ``--acl public-read`` as a flag for operations such as ``cp``, or ``aws
s3api put-object-acl`` and ``aws s3api get-object-acl`` to set set and get ACLs on existing objects.
