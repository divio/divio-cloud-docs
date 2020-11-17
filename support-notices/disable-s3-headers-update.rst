:orphan:

S3 media headers update causes problems during deployment
=========================================================

**Support notice 17th November 2020**


This notice applies to projects using :ref:`Aldryn Django <aldryn>` **only**.

S3 media headers update
========================================

During the deployment process of Aldryn Django projects, Aldryn Django applies a :ref:`release command
<release-commands>` to update S3 media headers with the appropriate caching settings. These headers are used by
Cloudflare when serving media.

The command is applied by `aldryn_config.py
<https://github.com/divio/aldryn-django/blob/support/2.2.x/aldryn_config.py#L521-L523>`_.


The problem
------------

If there are many media files, this process can take long enough that the deployment fails with a timeout.

In such circumstances, the process continues to run, and if a subsequent deployment is initiated, that will also fail,
this time immediately and with an unspecified error, for example::

    Deployment Error
    Error ID: f9dd23d378e8427296e5e4a6238af508


Solution
---------------------------

In almost all cases, S3 headers update can be disabled, by adding an :ref:`environment variable
<environment-variables>` to each environment affected:

* variable: ``DISABLE_S3_MEDIA_HEADERS_UPDATE``
* value: ``True``

This will cause the deployment process to skip the update.


Implications
-------------

Disable S3 media header updates will only have implications if you have applied custom media caching settings in
your own code. In all other cases disabling the update will have no implications.
