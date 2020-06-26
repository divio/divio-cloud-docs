.. _redirects:

HTTP redirects
===========================

Redirects in Divio projects will typically take place at one of two different levels:

* in the application code itself (for example, in Django or PHP)
* in the application's web gateway or server (for example, in uWSGI or Nginx)

.. mermaid::

    flowchart LR
      gateway <--> loadbalancers
      subgraph Customer application
        code(application code) <--> gateway(application gateway/server)
      end
      loadbalancers(Divio load balancers)

An application can blur the distinction between these two levels, but most will include distinct code and
gateway/server layers. Gateway/server-level redirects take place before a request reaches the application code (and
will therefore be faster and less expensive). However, code-level redirects are generally easier to implement.


Protocol redirects
------------------

Our projects are HTTPS-ready by default, and we provide free SSL certificates even on free projects.

To force redirect from HTTP to HTTPS: :ref:`Django <django_protocol_redirects>`, :ref:`Express JS
<how-to-express-js-https>`.


.. _301vs302:

301 Permanent vs 302 Temporary redirects
----------------------------------------

You will sometimes see online site-checking tools encouraging the use of
permanent redirects and even flagging temporary redirects as an issue. It is
true that a permanent redirect is sometimes more appropriate, but only when it
really should be permanent, and is **guaranteed** not to change.

Protocol, domain and language directs are ``302 Temporary`` by default. ``301
Permanent`` redirects are cached by browsers - some even update their bookmarks
if they encounter a ``301``. This can cause problems if the redirects change,
potentially causing redirect loops for users (which site owners will not be
able to replicate).
