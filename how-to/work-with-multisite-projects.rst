.. _set-up-multisite:

How to work with multi-site projects
====================================

Multi-site hosting, also known as *multi-tenancy*, makes it possible to host multiple sites,
serving multiple domains, using a single database.

..  note::

    This is distinct from serving a single site under multiple domains - this does not requite
    django-multisite, and only requires those domains to be set up in the Control Panel.

There are two ways of achieving this:

* multiple sites, one database, one project: :ref:`multisite-single-project`
* multiple sites, one database, multiple projects: :ref:`multisite-multiple-projects`


Logging in to multi-site instances
----------------------------------

In all multi-site projects, you will notice that each site requires its own log-in. Logging in to
one will not log you in to another. This is because the Django session cookie is *per-domain*.


.. _multisite-single-project:

Django Multisite
----------------

Our Django Multisite Plus allows you to serve multiple sites under multiple domains (including
sub-domains) from a single Divio Cloud Django project.

You need to inform us about each domain to be served. We will apply the configuration required,
which includes:

* installing and configuring Django Multisite Plus addon
* applying the necessary settings and environment variables

Because Live and Test servers use different domains, we provide a runtime module that sets up the
domain rewriting - via the ``Site`` model - appropriately in each case.

This will populate the Django Sites table (*Sites > Sites* in the admin), and the Django Multisite
Plus Sites table (*Multisite+ > Sites* in the admin), when the environment variable
``DJANGO_MULTISITE_PLUS_AUTO_POPULATE_SITES`` is ``True``.

In this case, **these auto-populated domains should not be edited manually**, as any changes will
simply be overwritten at the next deployment.


Switching between sites in a multi-site project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the simpler method and recommended unless you need to be able to switch often between sites.

Set a :ref:`local environment variable <local-environment-variables>`, ``SITE_ID``, to force
Django to serve a particular site. The site ID you need can be found in the list of Sites in the
admin.

After changing the ``SITE_ID`` you will neeed to restart the runserver for the change to take
effect.

If you set explictly set the ``SITE_ID`` this way, the next method will not work.


Option two: capture the sites' domains in ``/etc/hosts``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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


.. _multisite-multiple-projects:

Multiple Divio Cloud projects
-----------------------------

This method involves separate Django instances, one for each site. Its advantage is that it allows
you guarantee that each site will be served from a different instance, and it gives you more
control over the resources allocated to each site.

Set up your projects, including their domains, and then contact Divio support so we can configure
them all to use the same database and storage backend.

We will also advise on any other configuration you need to make.

..  important::

    It is **crucial** that you ensure all the projects sharing the same database use the same code,
    particularly around models. Otherwise, you could run into site errors or even database
    corruption problems, if model code is not in line with database table structure.

    You must take care to make and deploy code changes across sites in as consistent way as
    possible.

As each project runs separately, the easiest way to work on them locally is simply to launch
and stop each one as required.