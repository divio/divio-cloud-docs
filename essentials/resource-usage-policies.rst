.. _knowledge-resource-usage-policies:

Resource usage policies
=======================

Soft limits
-----------

We recognise that web applications can receive unexpected surges in traffic, and can sometimes exceed their
subscription's RAM, transfer or storage limits.

We operates a *soft limits* policy to ensure that your applications stay up. Even if you exceed the limits of your
subscription, your service won't be interrupted.

* RAM: we build in headroom above the advertised container allocation
* transfer, media and database storage: we do not enforce hard limits

If your project consistently consumes more than your plan, we'll get in touch to ask you to upgrade your plan
appropriately.


CDN and transfer volume calculations
------------------------------------

Divio projects automatically use CDN (content delivery networks) to optimise delivery of files from our site to your
users.

Your project's transfer volume will be calculated only on the traffic that we serve to the CDN - not the traffic that
the CDN serves to your users.
