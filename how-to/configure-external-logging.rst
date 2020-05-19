.. _configure-external-logging:

How to configure an external logging service
============================================

Your Test and Live servers have their own runtime logs, available from the project's dashboard in the Control Panel.

These logs are provided as a convenience. However they are limited to only the last 1000 lines of output and are not
intended to be a comprehensive logging system for production purposes.

For that we recommend subscribing to a dedicated logging service, of which there are several, and configuring your
project to route different kinds of logs (access, errors and so on) to different destinations, so you can use them more
effectively.

Example using LogDNA
--------------------

This document will show you how to set up logging using the popular LogDNA service. Using other services the principle
will be the same, with only some minor differences.

If you don't already have a LogDNA account, visit https://logdna.com and register for a free account. LogDNA will
provide you with an *ingestion key*.

Set your project up locally. We'll assume that you are using a standard Divio project using Aldryn Django.


Install the ``logdna`` Python library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need to add ``logdna`` to its requirements (strongly recommended: :ref:`pin it to a particular version
<pinning-dependencies-good-practice>`) and rebuild the project (``docker-compose build``).

This package provides a new logging handler (``logdna.LogDNAHandler``) that will forward log messages to LogDNA.


Amend the ``LOGGING`` configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Aldryn Django's ``aldryn.config.py``, you will find `the default logging configuration
<https://github.com/divio/aldryn-django/blob/support/2.2.x/aldryn_config.py#L317-L360>`_, that defines a ``LOGGING``
dictionary with several keys.

First, we'll add the new logging *handler* to this.

::

    LOGGING["handlers"]["logdna"] = {
            'class': 'logdna.LogDNAHandler',
            'key': '<insert your ingestion key here>',
            'options': {
                'hostname': 'your-website-name',
                'index_meta': True
            }
        }

What we have done here is added the new handler, ``logdna`` (the name doesn't actually matter) as a key to the dictionary.

Next, we need to configure the existing loggers, that actually produce the logs, to use the handler. In this example, we will append the ``logdna`` handler to the configuration of:

* the unnamed root logger ``""``
* the ``django`` logger
* the ``django.request`` logger

::

     LOGGING["loggers"][""]['handlers'].append('logdna')
     LOGGING["loggers"]["django"]['handlers'].append('logdna')
     LOGGING["loggers"]["django.request"]['handlers'].append('logdna')

More information about configuring Django logging can be found in :doc:`Django's logging documentation
<django:topics/logging>`.


Other logging options
---------------------

The above is just a very basic example of using external logging. We recommend becoming familiar with Django's logging
framework and configuring it to send the most useful logs for your purposes.


Sentry
~~~~~~

`Sentry <https://sentry.io>`_ is another popular service; `Aldryn Django is Sentry-aware
<https://github.com/divio/aldryn-django/blob/support/2.2.x/aldryn_config.py#L362-L363>`_ and requires only the
provision of a ``SENTRY_DSN`` environment variable to configure integration with Sentry.
