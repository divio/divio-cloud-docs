.. _caching:

Caching
=======

Database caching
----------------

Our default cache backend is `Django's database caching
<https://docs.djangoproject.com/en/1.10/topics/cache/#database-caching>`_; all
Divio Cloud projects are set up with this configured and ready to use.

This is a fast, scalable option, and is suited to most needs.

Database caching is shared by all instances of an application server.


Local per-instance caching
--------------------------

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
----------------------------

Other backends, such as `Redis <https://redis.io>`_ (a popular open-source
database) can be used as caching backends for Django.

If it suits your needs, you can procure a Redis or other caching instance from
a provider and use it with your Divio Cloud project.
