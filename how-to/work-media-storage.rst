.. _work-media-storage:

How to work with your project's media storage in Python applications
====================================================================

..  note::

    See also :ref:`interact-storage`.

Introduction
------------

Default file storage on Divio Cloud projects is handled by dedicated storage systems entirely
separate from the application.

In our architecture, The same site may be running as several different instances, on several
different application hosts (this is one reason why Divio Cloud projects can be scaled, because new
application instances can be created to meet increasing demand).

Although each of those instances will have its own local file storage, this will be independent of
each of the others, and it won't persist - once that instance ceases to exist, so will the files.
That storage will also be inaccessible to any other instances of the application.

This means a project applications can't expect to save files to its local storage, and then expect
to find them again.

Instead, the applications must use our storage services. These are `Amazon Web Services's S3
service <https://aws.amazon.com/s3/>`_, or a generic S3 hosting service via another provider.
Currently, most projects use Amazon's own S3 service, with the exception of projects in our Swiss
region.

For most Django applications, this won't require any additional work. Django is able to use
multiple storage backends, all addressed through a common API. This is the safe and correct way to
handle files in Django, so that applications can abstract from details of the storage
implementation, and simply not need to know about it.

As long as an application uses Django's storage API, rather than attempting to manipulate Python
File objects directly, it doesn't need to do anything differently.

Similarly, an application should not rely on knowing or manipulating a File object's file path.


Use ``DEFAULT_FILE_STORAGE``
----------------------------

Django's file storage system relies on the ``DEFAULT_FILE_STORAGE`` setting. Ideally, third-party
applications in your project should respect this for their own file handling.

This is not always the case however. In some cases the application may need to be configured
explicitly. More problematically, some applications may have hard-coded expectations for the file
storage system, and these will need to be rewritten.


Using Easy Thumbnails
~~~~~~~~~~~~~~~~~~~~~

Easy Thumbnails is the most widely-used image processing application in the Django ecosystem.

On Divio Cloud, ``THUMBNAIL_DEFAULT_STORAGE`` for Easy Thumbnails needs to be set explicitly, even
if ``DEFAULT_FILE_STORAGE`` has been set.

In most projects on Divio Cloud, Django Filer is installed. This takes care of the
``THUMBNAIL_DEFAULT_STORAGE`` - if Django Filer is installed, you don't need to do anything else to
use Easy Thumbnails correctly.

In the cases where it's not, it's necessary to do the same thing manually in the settings.py::

    # If the DEFAULT_FILE_STORAGE has been set to a value known by
    # aldryn-django, then use that as THUMBNAIL_DEFAULT_STORAGE as well.

    from aldryn_django import storage

    for storage_backend in storage.SCHEMES.values():
        if storage_backend == DEFAULT_FILE_STORAGE:
            THUMBNAIL_DEFAULT_STORAGE = storage_backend
            break
