.. _custom-domains:

Custom domains
===============

Depending on your subscription, custom domains can be served to *Live* servers of Divio projects by configuring the Control Panel and your DNS provider's settings.

..  note::

    The Test server will only use Divio's predefined URL.


DNS provider
-------------

We currently do not offer hosted DNS, so if your domain registrar does not offer DNS, you will need to use a third party
service such as `DNSimple.com <https://dnsimple.com/dashboard>`_.


Configuring DNS
----------------

In the Control Panel *Domains* view, add your custom domain, a root domain (e.g. example.com) or a subdomain. (e.g.
www.example.com or tutorial.example.com). The Control Panel will then display some suggested DNS configuration values
and report whether it has been configured correctly.

The Control Panel will also make automated checks. After a check fails, the domain will be checked every 15 minutes
until a correct set-up is detected. After a check finds it correct, checks will take place every 24 hours.

For a root domain (also known as a naked domain), they will include a suitable *ALIAS* configuration, and *A* records as
an alternative. We strongly recommend using *ALIAS* records over *A* records.

Some DNS providers don't support *ALIAS* records. In this case, for a root domain, use the IP addresses suggested by the
Control Panel in an *A* record. As the Control Panel suggests, these addresses could change in the future. However,
changes will be rare, and announced well in advance.

For a subdomain, only CNAMEs will be listed. 

.. note:: 
   
   If you accept the Divio Control Panel's suggested values, make sure to enter them appropriately. 
   
   You will not be able to simply paste as most DNS control panels will require you to enter the type of record, the
   name and the value into separate fields. 


Multiple domains
----------------

You need an entry in the Divio Control Panel for each domain, including subdomains, at which you want your site to be
available. An entry for example.com will not automatically enable www.example.com. If you want to serve your site at
both example.com and www.example.com you will need to add each to the Control Panel, and configure your DNS
appropriately.


Multiple projects on a root domain
-----------------------------------

You can if you wish run multiple Divio projects that are associated with the same root domain. For example, you might
have one project serving a site at example.com, another at intranet.example.com and another at trial.example.com.

That's fine - all you need to do is ensure that each has the appropriate domain or subdomain set in the Control Panel.


Redirects
----------

If you have multiple domains you will most likely want them to redirect to the primary domain. To set this, for each
secondary domain in the control panel, select the *Enable redirect* option. 

.. seealso::

  Our technical documentation for :ref:`redirects <redirects>`.


DNS provider settings
----------------------

Your DNS provider will be able to give advice on how to implement DNS settings.

Besides managing your DNS setting manually, we have introduced support for DNSimple's "one click services". This service
allows you to easily sync your domain settings with your Divio projects in a matter of a few clicks.

For this, login at `DNSimple.com <https://dnsimple.com/dashboard>`_, select your domain from the overview, navigate to
*Services* to *Add or edit services*.
 
In the *one-click services* overview, scroll down and add the *Divio Aldryn* service. Here you have to enter your *Divio
project domain* from your Divio project *Domains* view. 
