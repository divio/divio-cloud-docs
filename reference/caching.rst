.. _caching:

Caching in Divio Cloud applications
===================================

..  admonition:: See also

    * `Caching on Divio Cloud
      <http://support.divio.com/general/essential-knowledge-caching-in-divio-cloud-projects>`_

Caching in Divio Cloud applications will typically make use of :doc:`Django's own caching framework
<django:topics/cache>`.


Caching options
---------------

Database caching
~~~~~~~~~~~~~~~~

Our default cache backend is :ref:`Django's database caching <django:database-caching>`; all Divio
Cloud projects are set up with this configured and ready to use.

This is a fast, scalable option, and is suited to most needs.

Database caching is shared by all instances of an application server.


Local per-instance caching
~~~~~~~~~~~~~~~~~~~~~~~~~~

..  warning::

    Per-instance caching options are **not** suitable for django CMS sites,
    which require synchronisation of data across instances for correct
    operation.

    Depending on the needs of other applications, you may or may not find that
    these options are suitable.

Per-instance caching options cache data for a particular instance of the cloud
application server. This means that if your project is running on multiple
server instances, they will not share the caches.

For the same reason if you SSH into a Cloud server and do::

    from django.core.cache import cache

    cache.clear()

in a Python shell, you will only clear the cache in the container you have just
started up.

Options are:

* `local memory caching
  <https://docs.djangoproject.com/en/1.10/topics/cache/#local-memory-caching>`_
* `local filesystem caching <https://docs.djangoproject.com/en/1.11/topics/cache/#filesystem-caching>`_


Third-party caching backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Other backends, such as `Redis <https://redis.io>`_ (a popular open-source
database) can be used as caching backends for Django.

If it suits your needs, you can procure a Redis or other caching instance from
a provider and use it with your Divio Cloud project.


Caching in django CMS
---------------------

The Aldryn django CMS addon applies caching rules by default, via the
:setting:`django-cms:CMS_CACHE_DURATIONS` setting.

Control over caching settings is exposed in the Divio Cloud Control Panel in the configuration
options for Aldryn django CMS.

Defaults are to cache content for 60 seconds and menus for one hour.

It is often convenient to disable this while developing or working intensively on content. Adding::

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
