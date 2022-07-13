.. _caching:

Caching and CDN in `Divio <https://www.divio.com>`_ applications
================================================================

Infrastructure-level caching
----------------------------

As well as the caching and CDN (Content Delivery Network) we provide, you can also :ref:`apply your own
<apply-your-own-caching-cdn>`.

Caching is generally provided by `Cloudflare <https://cloudflare.com>`_. Other options can be provided or managed
on request.

Infrastructure-level caching is *URL-based*, and content-unaware - caching does not detect when files have changed.


.. _media-file-caching:

Media storage caching
~~~~~~~~~~~~~~~~~~~~~

Caching for media storage is automatically provided available on all applications and plans, and on Test as well as Live
servers. Note that this only includes files served from our media storage services (S3 buckets, Azure Blob storage
instances). Resources served by the application instances (HTML, static files) are not cached.

On request we can also provide Cloudflare `Polish
<https://support.cloudflare.com/hc/en-us/articles/360000607372-Using-Cloudflare-Polish-to-compress -images>`_ and
`Mirage <https://support.cloudflare.com/hc/en-us/articles/219178057-Configuring-Cloudflare-Mirage>`_ optimisation for
images.

..  note::

    Some of the media storage domains we use are not cached, including: ``sos-ch-dk-2.exo.io``, ``aldryn-media.io``,
    ``s3.amazonaws.com``.


Controlling caching headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cloudflare will cache media files according to the ``Cache-Control`` header applied to the files. For example:

..  code-block:: text

    cache-control: max-age=3600

will set a TTL of one hour (3600 seconds).

Your application can set these headers when managing the file storage.


In Aldryn Django (legacy)
..............................

Aldryn Django does this by default, also
applying some sensible default values (see also :ref:`DISABLE_S3_MEDIA_HEADERS_UPDATE`).

Our Aldryn Django Filer addon `applies a one-year TTL to its public thumbnail files
<https://github.com/divio/django-filer/blob/master/aldryn_config.py#L22-L27>`_ using the
``MEDIA_HEADERS`` setting. In turn, our Aldryn Django addon applies the ``MEDIA_HEADERS`` values it
discovers to `the media storage class that configures the S3 bucket
<https://github.com/divio/aldryn-django/blob/support/2.2.x/aldryn_django/storage.py#L29-L74>`_.


Application content caching
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can also provide managed caching of application content (including custom page rules) using Cloudflare or other
services, on request.

..  seealso:: :ref:`Cache invalidation control via the Divio application Dashboard
  <how-to-manage-cloudflare-cache>`


.. _apply-your-own-caching-cdn:

Applying your own caching/CDN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may also provide your own caching and CDN.

**For media files**, if you are using our media domain (the default), your applications will automatically use the CDN
we provide and this cannot be changed. However, it's also possible to use your own domain (see for example
:ref:`how-to-configure-media-serving-custom-domain`) for media, in which case you are free to use what you wish.

**For other resources** (served by the containers) you can set up another CDN, for example using your own Cloudflare
account. In such a case you should inform us so that instead of providing a certificate automatically ourselves, you
can upload your own manually.


In-application caching
-------------------------

Caching in your application is up to you and the stack you are using. For example, Django applications will typically
make use of :doc:`Django's own caching framework <django:topics/cache>`.


Application caching options
~~~~~~~~~~~~~~~~~~~~~~~~~~~

What *not* to use in your code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Caching should rely on a shared store that persists for all containers. For example, caching that
relies on a container's local file-system or local memory should not be used, as only that
container (and not a container running in parallel, or one instantiated later) will be able to
access the items it stores.

In some cases, this can simply lead to inefficiency (not using cached data). In other cases, it
could cause malfunction or even data-loss, if two instances are working with inconsistent data.


Database caching
~~~~~~~~~~~~~~~~

Database caching is shared by all instances of an application server. It's a fast, scalable option, and is suited to
most needs.


Third-party caching backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other backends, such as `Redis <https://redis.io>`_ (a popular open-source
database) can be used as caching backends for Django.

If it suits your needs, you can procure a Redis or other caching instance from
a provider and use it with your Divio application.


Caching with Aldryn Django (legacy)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Database caching is the default cache backend for Aldryn Django applications, with
:ref:`Django's database caching <django:database-caching>` configured and ready to use.

The Aldryn django CMS addon applies additional caching rules by default, via the
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

to the application's ``settings.py`` will disable all caching in the CMS in the local and Test
environments.
