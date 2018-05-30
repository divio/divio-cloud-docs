.. _set-up-multisite:

How to work with multi-site projects
====================================

Multi-site hosting, also known as *multi-tenancy*, makes it possible to host multiple sites,
serving multiple domains, using a single database.

..  note::

    This is distinct from serving a single site under multiple domains - this does not requite
    django-multisite, and only requires those domains to be set up in the Control Panel.

There are two ways of achieving this:

* multiple sites, one database, one project, :ref:`multisite-single-project`
* multiple sites, one database, multiple projects :ref:`multisite-multiple-projects`


Logging in to multi-site instances
----------------------------------

In all multi-site projects, you will notice that each site requires its own log-in. Logging in to
one will not log you in to another. This is because the Django session cookie is *per-domain*.


Switching between sites in a multi-site project
-----------------------------------------------

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


Forcing the site with an environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first is to set a :ref:`local environment variable <local-environment-variables>`, ``SITE_ID``,
that forces Django to serve a particular site. The site ID you need can be found in the list of
Sites in the admin.

After changing the ``SITE_ID`` you will neeed to restart the runserver for the change to take
effect.

If you set explictly set the ``SITE_ID`` this way, the next method will not work.


Capturing the sites' domains in ``/etc/hosts``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  todo:: I can't get this to work so far

The other method is to point all the domains you need to handle locally to ``localhost``. For
example, for each of the domains in the table above, you could add an entry in your ``/etc/hosts``
file::

    localhost   example.de
    localhost   example.gh
    localhost   example.us

Now, each domain will resolve to ``localhost``, and the server running there will also be able to
use the information contained in the request to serve the required site.

Using this method, you can readily switch between sites using the standard site-switching
functionality. The site-switching links will refer to the various Live sites, but these addresses will be intercepted by the modified ``hosts`` file.

..  note::

    If the port on which you access local sites is not 80, you will need to append this to the
    addresses you require.

This method is more convenient if your local development work requires you to switch sites, but you
must remember to remove the entries from ``hosts`` once you've finished.

Note also that if you force the site using the environment variable method, then this method will
not work.


.. _multisite-single-project:

Django Multisite
----------------

`.django-multisite <https://github.com/ecometrica/django-multisite>`_ will allow you to serve
multiple sites under multiple domains (including sub-domains) from a single Divio Cloud Django
project.

You need to inform us about each domain to be served. We will apply the configuration required.

This includes the installation and configuration of the Django Multisite Plus addon, as well as
applying the necessary settings and environment variables.

Because live and stage use different domain, we provide a runtime module that sets up the domain
rewriting - via the ``Site`` model - appropriately in each case.

This will populate the Django Sites table (*Sites > Sites* in the admin), and the Django Multisite
Plus Sites table (*Multisite+ > Sites* in the admin), when the environment variable
``DJANGO_MULTISITE_PLUS_AUTO_POPULATE_SITES`` is ``True``.

In this case, **these auto-populated domains should not be edited manually**, as any changes will
simply be overwritten at the next deployment.


.. _multisite-multiple-projects:

Multiple Divio Cloud projects
-----------------------------

..  todo:: To be completed
