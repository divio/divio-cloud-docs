..  Do not change the filename of this document
    Referred to by: tutorial message 160 https://control.divio.com/admin/tutorial/message/160
    Where: in the Domains view e.g. https://control.divio.com/control/1234/edit/5678/domains/
    As: https://docs.divio.com/en/latest/background/domains/

.. _redirects:
.. _domains:

Domains
===========================

An application's domains are managed in the *Domains* view (or via the :ref:`Divio API <use-divio-api>`).

.. image:: /images/domains.png
   :alt: 'Domains'
   :class: 'main-visual'

--------

As well as the user-managed domains, which apply only to the Live environment, each environment of each application
also has a fixed Divio-provided domain, for example ``example.aldryn.io`` or ``example-stage.stage.aldryn.io``. The
ingress controller uses this information to route requests to particular applications.

The Control Panel interface shows whether DNS has been correctly configured for each domain, and whether
valid SSL certificates are in place.


DNS records
~~~~~~~~~~~

For bare domains (e.g. ``example.com``) we recommend using the ALIAS records suggested in the Control Panel interface.
Not all DNS providers support ALIAS records, in which case, A records may be used. Note however that the IP addresses
we use may change, so we recommend using ALIAS records over A records where possible.


SSL certificates
~~~~~~~~~~~~~~~~

We provide free SSL certificates automatically for all domains using our default domain backend. Other options are
available on request, as well as the option to upload your own certificate.

A certificate can only be applied if the domain passes automated DNS configuration tests. Once a domain is added, a
check takes place. If a check fails, the domain will be checked every 15 minutes until a correct set-up is detected.
Once a check finds it correct, subsequent checks take place every 24 hours.


.. _domain-settings-and-env-vars:

Domain settings and environment variables
------------------------------------------

As well as providing routing to applications, domain settings also set environment variables that the applications can
make use of internally. These environment variables are:

* ``DOMAIN`` - the domain that is marked as *Primary* in the interface
* ``DOMAIN_ALIASES`` - each of the other listed domains, except for those in:
* ``DOMAIN_REDIRECTS`` - any domains that have the *Redirect* setting enabled, i.e. that should redirect to ``DOMAIN``

Once the settings have been applied in the interface, the environment variables are also set - there is no need to
add them manually. The values will not be available to any running environments until they have been redeployed.

Your application may need to use these variables to function correctly. For example, a Django application has an
``ALLOWED_HOSTS`` :ref:`setting <deploy-django-security>`, listing the hosts that the application can be served from. This needs to list all the
domains applied in the interface, and made available via ``DOMAIN``, ``DOMAIN_ALIASES`` and ``DOMAIN_REDIRECTS``. 


..  important::

    It is up to the application to read and make use of these environment variables correctly. For example,
    an application will not automatically redirect to the primary domain from another unless it can read the
    environment variables and apply the appropriate configuration.

    (This doesn't apply to legacy Aldryn Django applications, which will configure themselves automatically using
    these variables. See :ref:`redirects in Aldryn Django projects <django-manage-redirects>`.)


Redirects
-----------

Redirects in applications will typically take place at one of two different levels:

* in the application code itself (for example, in Django or PHP)
* in the application's web gateway or server (for example, in uWSGI or Nginx)

.. mermaid::

    flowchart LR
      gateway <--> ingress-controller
      subgraph Customer application
        code(application code) <--> gateway(application gateway/server)
      end
      ingress-controller(Divio load-balancers)

An application can blur the distinction between these two levels, but most will include distinct code and
gateway/server layers. Gateway/server-level redirects take place before a request reaches the application code (and
will therefore be faster and less expensive). However, code-level redirects are generally easier to implement, and the
overhead of handling them is minimal.


Protocol redirects
~~~~~~~~~~~~~~~~~~~

To redirect from HTTP to HTTPS: :ref:`Django <django_protocol_redirects>`, :ref:`Express JS
<how-to-express-js-https>`.


.. _301vs302:

301 Permanent vs 302 Temporary redirects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will sometimes see online site-checking tools encouraging the use of
permanent redirects and even flagging temporary redirects as an issue. It is
true that a permanent redirect is sometimes more appropriate, but only when it
really should be permanent, and is **guaranteed** not to change.

Protocol, domain and language directs are ``302 Temporary`` by default. ``301
Permanent`` redirects are cached by browsers - some even update their bookmarks
if they encounter a ``301``. This can cause problems if the redirects change,
potentially causing redirect loops for users (which site owners will not be
able to replicate).
