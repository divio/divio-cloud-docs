.. _infrastructure-ip-addresses:

IP addresses
===============================

Divio's containerised infrastructure is distributed over a number of geographical and vendor based regions. At any one
time, the servers within each region are allocated an IP address from that region's range.

Servers in our infrastructure (application builders and runners, and other services) are not permanent hosts but
short-lived instances that can be provisioned at a moment's notice and are regularly recycled.

An IP address within a particular pool can therefore be reallocated to a different server at any time, and there is no
guarantee that a server's address will remain the same from one moment to another.

In addition, vendors' IP ranges themselves are not guaranteed and can be subject to change regularly and frequently,
sometimes without notice.

Finally, even if a server's IP remains the same, an application might be moved to a different server at any time.

This means that **IP addresses are not to be relied upon as a means of reaching or identifying Divio applications or
servers**.


Load-balancer IP addresses
--------------------------

A partial exception to this is the IP addresses of our load-balancers, which can be regarded as semi-static.

Customers' projects may be attached to domains for which CNAMES cannot used (that is, bare domains such as
``example.com``, rather than sub-domains such as ``www.example.com``). In this case we recommend using ALIAS records.
Not all DNS providers support ALIAS, and in those cases it is necessary to use A records, which require IP addresses.

We take efforts to keep our load-balancers in each region on a very small number of IP addresses so that A records can
rely on them. All the same, even these occasionally must be amended. In that event affected customers are informed in
advance to minimise disruption.


Implications for customer projects
----------------------------------

Occasionally a fixed IP address for a customer's project might be desired for:

* incoming connections, such as a client connection to an API running in the project
* outgoing connections, such as a connection to an external API, where the IP address is required for whitelisting
  purposes

For in-bound connections, our semi-static load-balancer IP addresses can be an adequate way of routing connections to a
customer application, as long as the user remains aware that these addresses may need to be changed in the future.

Out-bound connections present more challenge. Cloud-based hosting is very well established, and very few services still
insist upon using IP addresses as a way of guaranteeing the originator of a connection. However, IP addresses are
widely used in firewall rules, and this can still present an issue (see below for other options).

In general though, an alternative, better of achieving a connection to or from Divio applications can and should be
found.


.. _infrastructure-ip-fixed-addresses:

Other options
-------------

In some cases, it may be strictly necessary for an application running on Divio to present an unvarying IP address or
range of addresses to an external service.

In such cases, for projects running in private regions only, a number of solutions can be implemented:

* a dedicated proxy to redirect traffic from a fixed IP address to the application
* a NAT gateway with a fixed external IP address
* a dedicated site-to-site VPN

Please contact Divio support to discuss these options.


IPv6 support
------------

We do not currently support IPv6 on our infrastructure, as IPv6 is not yet supported in key components provided by our
vendors. Future IPv6 support will be introduced when possible.
