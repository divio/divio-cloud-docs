..  Do not change this document name!
    Referred to by: tutorial message 134 project-create-base-project
    Where: when switching regions or plans
    As: https://docs.divio.com/en/latest/background/maintenance/#cloudshift

.. _maintenance:

Maintenance operations
==================================

Most operations that take place on Divio projects can be considered routine operations, and will not under normal
circumstances interrupt the function of web applications.

Some however by their nature are more complex and can require a brief downtime. The most notable example is deployments
that require a change of deployment region, such as :ref:`cloudshift operations (below) <maintenance-cloudshift>`. These
are regarded as *Maintenance operations*.

..  image:: /images/maintenance-window.png
    :alt: 'Maintenance window'


Maintenance windows
-------------------

Maintenance operations will only take place during designated weekly maintenance windows, to control when downtime
occurs.

By default, a site's maintenance window is set to hours UTC 01:00-05:00 each Monday, but this can be changed to suit
your business needs. A queued maintenance action can also be triggered manually using the *Start now* option to run
immediately, outside the window.


..  Do not change this heading name (see above).

.. _maintenance-cloudshift:

Cloudshift region migration
------------------------------

Moving your project from one region to another requires a *cloudshift* migration operation. As well as entailing a short
downtime, it may also require amending external services such as DNS that need to identify the application.

The region migration operation will be performed during a maintenance window.

In the case of DNS changes, we advise reducing DNS TTLs well in advance of the migration, so that when DNS entries
are changed, disruption is minimised.

Note that a cloudshift operation deploys any outstanding commits on the project's environments, *even if they were not
previously deployed*.
