.. _caching:

Caching in Divio projects
===================================

Infrastructure-level caching
----------------------------

Caching is provided by `Cloudflare <http://cloudflare.com>`_. Caching is provided on all projects
and plans, and on Test as well as Live servers. It's automatic and requires no additional action or
configuration.


Defaults
~~~~~~~~

By default, only files served from our media buckets (typically images) are cached. Resources
served by the application instances (HTML, static files) are not cached.

Files are cached indefinitely; the cache is not invalidated automatically when a file is
changed, unless its URL is changed.

Caching is URL-based, and wholly content-unaware - the caching system does not detect when files
have changed.


Options
~~~~~~~

However, other options for caching are available on request (on eligible projects only). This
includes:

* caching of application content as well as media files
* Cloudflare `Polish
  <https://support.cloudflare.com/hc/en-us/articles/360000607372-Using-Cloudflare-Polish-to-compress
  -images>`_ and `Mirage
  <https://support.cloudflare.com/hc/en-us/articles/219178057-Configuring-Cloudflare-Mirage>`_
  optimisation for images
* `cache invalidation control via the Divio project Dashboard
  <https://support.divio.com/en/articles/3414982-how-to-clear-the-cloudflare-cdn-cache>`_
* custom Cloudflare page rules


Media file caching
~~~~~~~~~~~~~~~~~~

Typically, the bulk of a page web's transfer load is accounted for by its media files, most of
which will be images in the page.

All media files are handled by our dedicated storage and hosting providers, using S3 buckets.

Delivery of these files is handled by Cloudflare's CDN, which also caches the files. Cloudflare
will cache media files according to the ``Cache-Control`` header applied to the files.

For example:

..  code-block:: text

    cache-control: max-age=3600

will set a TTL of one hour (3600 seconds).


Controlling caching headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For an example: our Aldryn Django Filer addon `applies a one-year TTL to its public thumbnail files
<https://github.com/divio/django-filer/blob/master/aldryn_config.py#L22-L27>`_ using the
``MEDIA_HEADERS`` setting. In turn, our Aldryn Django addon applies the ``MEDIA_HEADERS`` values it
discovers to `the media storage class that configures the S3 bucket
<https://github.com/divio/aldryn-django/blob/support/2.2.x/aldryn_django/storage.py#L29-L74>`_.

Any application that needs to control the behaviour of cached media will need either to make use
of the provided functionality in Aldryn Django, or configure the S3 bucket directly itself.


Application-level caching
-------------------------

Django applications
~~~~~~~~~~~~~~~~~~~

Caching in Divio Django applications will typically make use of :doc:`Django's own caching framework
<django:topics/cache>`.


Caching in django CMS
^^^^^^^^^^^^^^^^^^^^^

The Aldryn django CMS addon applies caching rules by default, via the
:setting:`django-cms:CMS_CACHE_DURATIONS` setting.

Control over caching settings is exposed in the Divio Control Panel in the configuration
options for Aldryn django CMS. Defaults are to cache content for 60 seconds and menus for one hour.

It is often convenient to disable caching while developing or working intensively on content. Adding::

    import os
    env = os.getenv
    STAGE = env('STAGE', 'local').lower()
    if STAGE in {'local', 'test'}:
        CMS_PAGE_CACHE = False
        CMS_PLACEHOLDER_CACHE = False
        CMS_CACHE_DURATIONS = {
            'menus': 0,
            'content': 0,
            'permissions': 0,
        }

to the project's ``settings.py`` will disable all caching in the CMS in the local and Test
environments.


Application caching options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

What *not* to use
^^^^^^^^^^^^^^^^^

Caching should rely on a shared store that persists for all containers. For example, caching that
relies on a container's local file-system or local memory should not be used, as only that
container (and not a container running in parallel, or one instantiated later) will be able to
access the items it stores.

In some cases, this can simply lead to inefficiency (not using cached data). In other cases, it
could cause malfunction or even data-loss, if two instances are working with inconsistent data.


Database caching
~~~~~~~~~~~~~~~~

Database caching is shared by all instances of an application server, making database caching
suitable for many use-cases.

It's our default cache backend for Django projects - all Divio Django projects are set up with
:ref:`Django's database caching <django:database-caching>` configured and ready to use.

This is a fast, scalable option, and is suited to most needs.


Third-party caching backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other backends, such as `Redis <https://redis.io>`_ (a popular open-source
database) can be used as caching backends for Django.

If it suits your needs, you can procure a Redis or other caching instance from
a provider and use it with your Divio project.
