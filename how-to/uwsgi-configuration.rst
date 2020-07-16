.. gateway-configuration:

How to manage uWSGI configuration
=================================

In our Django projects, the uWSGI gateway to the load balancers is part of the customer application:

.. mermaid::

    flowchart LR
      gateway <--> loadbalancers
      subgraph Customer application
        code(Django) <--> gateway(uWSGI)
      end
      loadbalancers(Divio load balancers)

uWSGI is already configured and optimised in these projects. Most of this configuration is managed by :ref:`Aldryn
Django <aldryn-django>`; see also :ref:`live-performance`.

All of uWSGI's configuration can be managed entirely within the project, according to your own requirements, but be
warned that misconfiguration can be severely detrimental to an application's performance.


..  _uwsgi-configuration:

uWSGI environment variables
---------------------------

uWSGI offers `a vast number of configuration variables <http://uwsgi-docs.readthedocs.io/en/latest/Options.html>`_. Any
one of them can be set using an environment variable starting ``UWSGI_``, followed by the name of the variable in
uppercase.

For example, the ``processes`` variable can be configured by setting ``UWSGI_PROCESSES``.

Generally you will not need to touch these variables, and we recommend leaving them alone unless you need to change
something and you know what you are doing.


uWSGI buffer size
~~~~~~~~~~~~~~~~~

One setting that occasionally needs to be adjusted is ``UWSGI_BUFFER_SIZE``. The default value is ``4096``. If your
site has to deal with very large request headers, you may receive a ``web invalid request block size`` error in your
project's logs.

In this case, you can increase the buffer size to allow larger request headers. (You may also want to find out why your
site is running into such large request headers - for example, its cookies may be excessively large.)


.. _uwsgi-more-complex-configuration:

More complex configuration
-------------------------------

The uWSGI gateway can handle requests before they reach your application's code, which is faster and less expensive
than doing it in, say, Django (though not as convenient).

The configuration of this behaviour is often too complex to be expressed in simple environment variables; instead, it
can be achieved by including a uWSGI configuration file.

The uWSGI configuration file needs to be specified using uWSGI's ``include`` option, i.e. with the ``UWSGI_INCLUDE``
environment variable. For example::

  UWSGI_INCLUDE=uwsgi.ini

Then the file can contain the additional configuration required.

It is beyond the scope of this documentation to discuss this in detail, but a typical use-case would be to perform a
redirect. In such a case you could add a rule to the ``uwsgi.ini`` file specified above::

  [uwsgi]
  route = old rewrite:new

(This will redirect a request from ``old`` to ``new``.)
