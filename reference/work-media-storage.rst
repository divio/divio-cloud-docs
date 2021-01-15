.. _work-media-storage:

Working with your project's media storage in Python applications
====================================================================

..  seealso:::

    * :ref:`interact-storage`

.. _work-media-storage-introduction:

Introduction
------------

Default file storage on Divio projects is handled by dedicated storage systems entirely
separate from the application.

In our architecture, the same site may be running as several different instances, on several
different application hosts (this is one reason why Divio projects can be scaled, because new
application instances can be created to meet increasing demand).

Although each of those instances will have its own local file storage, this will be independent of
each of the others, and it won't persist - once that instance ceases to exist, so will the files.
That storage will also be inaccessible to any other instances of the application.

This means a project's applications, cron jobs or other process can't expect to save files to its
local storage, and then expect to find them again.


Our storage service providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead, the applications must use our storage services. These are `Amazon Web Services's S3
service <https://aws.amazon.com/s3/>`_, or a generic S3 hosting service via another provider.
Currently, most projects use Amazon's own S3 service, with the exception of projects in our Swiss
region.


Working with our storage backends in Django
---------------------------------------------

For most Django applications, this won't require any additional work. Django is able to use
multiple storage backends, all addressed through a common API. This is the safe and correct way to
handle files in Django, so that applications can abstract from details of the storage
implementation, and simply not need to know about it.

As long as an application uses Django's storage API, rather than attempting to manipulate Python
File objects directly, it doesn't need to do anything differently.

Similarly, an application should not rely on knowing or manipulating a File object's file path.


Use Django's defined ``DEFAULT_FILE_STORAGE``, not ``FileSystemStorage``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your code may use Django's :mod:`FileSystemStorage <django:django.core.files.storage>`. This
provides basic file storage, on a filesystem local to the code. For the reasons described in the
:ref:`Introduction <work-media-storage-introduction>` it is therefore not suitable for use on
Divio.

Instead, you must use the storage as defined by Django's ``DEFAULT_FILE_STORAGE`` - which you can
do simply by not explicitly specifying a storage system, and using
``django.core.files.storage.default_storage``.

See also :ref:`Django's discussion <django:file storage systems>` of the subject.


File storage in third-party applications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ideally, third-party applications in your project should respect this for their own file handling.

This is not always the case however. In some cases the application may need to be configured
explicitly. More problematically, some applications may have hard-coded expectations for the file
storage system, and these will need to be rewritten.


Private file storage
~~~~~~~~~~~~~~~~~~~~

Our storage backend does not support private file storage (i.e. requiring authentication) on S3
objects.

If you need private storage, you can define an additional Django storage backend in your project,
which sets S3 objects to be private as required.

Whenever you need to manage private files, you will need to invoke this custom backend.

The backend can use the buckets we provide to do this, but please be aware that if you restore a
backup, or use our tools to push files, *all the files will become public*.

Alternatively, you can use a bucket of your own with this backend.


Using Easy Thumbnails
~~~~~~~~~~~~~~~~~~~~~

Easy Thumbnails is the most widely-used image processing application in the Django ecosystem.

On Divio, ``THUMBNAIL_DEFAULT_STORAGE`` for Easy Thumbnails needs to be set explicitly, even
if ``DEFAULT_FILE_STORAGE`` has been set.

In most projects on Divio, Django Filer is installed. This takes care of the
``THUMBNAIL_DEFAULT_STORAGE`` - if Django Filer is installed, you don't need to do anything else to
use Easy Thumbnails correctly.

In the cases where it's not, it's necessary to do the same thing manually in the ``settings.py``::

    # If the DEFAULT_FILE_STORAGE has been set to a value known by
    # aldryn-django, then use that as THUMBNAIL_DEFAULT_STORAGE as well.

    from aldryn_django import storage

    for storage_backend in storage.SCHEMES.values():
        if storage_backend == DEFAULT_FILE_STORAGE:
            THUMBNAIL_DEFAULT_STORAGE = storage_backend
            break


Loading media files into your applications' pages
-------------------------------------------------

Sometimes an application in your project will need to load media files using JavaScript.

Since your media files are held on a server under a different domain from the application,
browsers may refuse to allow this cross-domain loading for security reasons.

There are two solutions to this.


Load media from ``static``
~~~~~~~~~~~~~~~~~~~~~~~~~~

One is to make sure that all files you need to load are in your site's *static* files,
rather than media. (The static files are served from the same domain as the application itself, so
browsers will be able to load files using JavaScript without complaint).

This has the advantage of not running into the possibility of using JavaScript to load
user-submitted material (which could include material uploaded by untrusted users).


Enable CORS headers
~~~~~~~~~~~~~~~~~~~

The other solution is to :ref:`enable CORS ("cross-origin resource sharing") headers <interact-storage-cors>` on the media bucket, allowing the bucket to serve its resources when
requested by a page on a different domain.


Storage speed and performance
-----------------------------

Note that if you need to make many read/write operations to file storage, or are working with very
large objects, that the speed you experience on the cloud can be considerably less than what you
experience in the local development environment.

The local development environment has the advantage of locally-attached storage, and should not
necessarily be taken as a guide to performance on the cloud.

*In most cases, this won't actually matter.* However, if your code works very intensively with
storage, it can be more efficient and faster to do all that work on the application instance's own
local filesystem, in a temporary directory, and then send the finished work to the remote storage.
