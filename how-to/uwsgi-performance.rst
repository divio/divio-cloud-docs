.. _live-performance:

How to fine-tune your server's performance
==========================================

In the `Divio <https://www.divio.com>`_ Control Panel for your application, you can easily change the resources 
(instances, RAM, storage, transfer) allocated to your application to adjust for its needs.

In most cases, having chosen suitable values for these, you won't need to make further changes.

If however your application has unusual demands or sees unusual traffic, you can also fine-tune some
settings to match its needs even better.

Optimising the settings for a high-traffic site isn't just a case of allocating more resources
indiscriminately on the basis that "more is better".

For example, a site that sees *large numbers* of requests that each represent a *low load* will
benefit from being allowed to serve more concurrent requests, but that could make things worse for
a site that sees a *smaller number* of requests each representing a *heavier load*.


Monitoring and profiling
------------------------

Our Control Panel's metrics will give you a basic idea of RAM usage. However, there are more
sophisticated tools available that can give you much more, and more finely-grained, information.

These range from Python libraries (such as `memory-profiler
<https://pypi.python.org/pypi/memory_profiler>`_ or `line_profiler
<https://pypi.org/project/line_profiler/>`_) to third-party monitoring/profiling services.


.. _aldryn-django-performance-settings:

Aldryn Django settings
----------------------

The :ref:`Aldryn Django addon <aldryn-django>` is responsible for ensuring that uWSGI (the
application gateway server) starts up with appropriate parameters, for example for :ref:`static
file caching control <static-file-cache-control>`.

These parameters can be controlled by environment variables.

..  note::

    Some of these environment variables represent uWSGI runtime options. It's also possible to
    configure :ref:`other uWSGI settings <uwsgi-configuration>`, but we don't recommend doing so
    unless you are familiar with them already and understand their implications.


Increase ``DJANGO_WEB_WORKERS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, each instance can can run three concurrent uWSGI web workers, in other words, three concurrent web processes (note that your plan may include multiple instances). This is determined by ``DJANGO_WEB_WORKERS``.

Increasing the number of web workers will allow you to serve more concurrent requests. Note that
this will increase the RAM consumption of each instance, so make sure you monitor the results over
time (briefly exceeding your hosting plan's RAM limits might not matter, but if this is sustained,
you will need to upgrade to a higher plan).

You can calculate as follows: *requests per second* * *average time to serve a request (in seconds)* will give you a
rough idea how many concurrent web workers your sight needs.

Three uWSGI web workers is quite a conservative number. You are likely to find that you can safely double the number of
web workers. Increase them in small increments, and back off if you find that RAM consumption becomes excessive.

You are unlikely to see any benefit from lowering ``DJANGO_WEB_WORKERS`` below the default.


Increase or decrease ``DJANGO_WEB_MAX_REQUESTS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see more RAM use than expected, try lowering ``DJANGO_WEB_MAX_REQUESTS``. This controls the
number of requests each worker serves before it is recycled (replaced by a fresh one).

There is a small overhead in replacing the worker. Typically - unless you are seeing excessive RAM
usage - increasing this number can improve performance. A value of 3000 is a reasonable
starting-point for experimenting with different values.

*Lowering* this number can help when requests are memory-hungry, because recycling the worker
releases the RAM.


Decrease ``DJANGO_WEB_TIMEOUT``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default allowable lifetime of a web process is 120 seconds. After this period, the worker
handling it will be recycled.

You can lower this, if you know that no request served by your site should expect to take longer
under normal circumstances. It means that the process that is slow or held up will be dropped,
but will allow the site to try again, or serve other requests.

Taking this as low as 10 seconds may have benefits with no adverse effects. If your site
occasionally needs to serve views that entail long processes (for example, applying a filter on a
huge admin list) then you will need to adjust it upwards appropriately.


Disable or reconfigure ``UWSGI_CHEAPER`` (uWSGI cheaper mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, applications use `uWSGI's cheaper mode <https://uwsgi-docs-additions.readthedocs.io/en/latest/Cheaper.html>`_.

When the site is idling in cheaper mode, uWSGI will dismiss unneeded web workers. This saves RAM, and is the
recommended configuration for most applications. In some circumstances however it can be advantageous to disable this 
mode, or adjust its settings.

This is generally only applicable to constant high-traffic sites. Please take care if you feel you need to
disable cheaper mode or modify its settings, as misconfiguration can have adverse results.
