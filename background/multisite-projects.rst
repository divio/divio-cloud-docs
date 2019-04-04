.. _multisite-projects:

Multi-site projects on Divio Cloud
==================================

Multi-site hosting, also known as *multi-tenancy*, makes it possible to host multiple sites,
serving multiple domains, using a single database.

..  note::

    This is distinct from serving a *single site* under *multiple domains* - this does not require django-multisite,
    and only requires those domains to be set up in the Control Panel.

We support two multi-site options:

* our fully-supported Django Multisite+ addon, available for qualifying projects only
* a DIY implementation via the `django CMS Multisite package <https://pypi.org/project/djangocms-multisite/>`_

Multi-site functionality is available only for Business plan projects that meet certain criteria. Please contact Divio
support for more details.


Fully supported Django Multisite+ option
----------------------------------------

This is the easiest way to set up multi-site projects on Divio Cloud.

We will install and configure Django Multisite+.

You need to inform us about each domain to be served. We will apply the configuration required,
which includes:

* installing and configuring Django Multisite Plus addon
* applying the necessary settings and environment variables


DIY implementation
------------------

You will need to install `django CMS Multisite package <https://pypi.org/project/djangocms-multisite/>`_ and manage any
settings and configuration manually.

We are able to assist by setting up your Test server domains, but other than that we are not able
to provide support for this option.


Logging in to multi-site instances
----------------------------------

In all multi-site projects, you will notice that each site requires its own log-in. Logging in to
one will not log you in to another. This is because the Django session cookie is *per-domain*.


Switching between sites in a local multi-site project
-----------------------------------------------------

Suppose you have a multi-site project ``example-stage.eu.aldryn.io`` whose domains are configured
thus:

=======  ==========  =============================
Site     Live        Test
=======  ==========  =============================
Germany  example.de  de.example-stage.eu.aldryn.io
Ghana    example.gh  gh.example-stage.eu.aldryn.io
USA      example.us  us.example-stage.eu.aldryn.io
=======  ==========  =============================

On both the Test and Live Cloud servers, domain routing will be configured by us and will work
automatically.

Locally, more work is required, as each of the sites will be served at the same address (i.e.
``localhost``). Unlike the Cloud set-up, your local environment has no way to route different
requests to different sites - because the request for ``localhost`` doesn't contain the domain
information needed to do this.

Instead, you will need to handle multi-site routing manually.

There are two approaches you can take:


Option one: Force the site with an environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the simpler method and recommended unless you need to be able to switch often between sites.

Set a :ref:`local environment variable <local-environment-variables>`, ``SITE_ID``, to force
Django to serve a particular site. The site ID you need can be found in the list of Sites in the
admin.

After changing the ``SITE_ID`` you will neeed to restart the runserver for the change to take
effect.

If you set explictly set the ``SITE_ID`` this way, the next method will not work.


Option two: capture the sites' domains in ``/etc/hosts``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The other method is to point all the domains you need to handle locally to ``localhost``. For
example, for each of the domains in the table above, you could add an entry in your ``/etc/hosts``
file::

    localhost   example.de
    localhost   example.gh
    localhost   example.us

These should match the domains as they appear in the admin at *Sites > Sites*.

Now, each domain will resolve to ``localhost``.

It will help to have your local site served on port 80, so in the :ref:`docker-compose file
<docker-compose-yml-reference>`, set::

    ports:
     - "80:80"

for the ``web`` service.

The local Divio environment server running will now be able to use the information contained in the
request for say example.de or example.gh to serve the required site.

Using this method, you can readily switch between sites using the standard site-switching
functionality. The site-switching links will refer to the various Live sites, but these addresses will be intercepted by the modified ``hosts`` file.

..  note::

    If the port on which you access local sites is not 80, you will need to append this to the
    addresses you require.

This method is more convenient if your local development work requires you to switch sites, but you
must remember to remove the entries from ``hosts`` once you've finished.

Note also that if you force the site using the environment variable method, then this method will
not work.
