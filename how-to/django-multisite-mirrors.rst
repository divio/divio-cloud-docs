..  Do not change this reference!
    Referred to by: user support guides
    Where: in essential-knowledge/mirrors.rst
    As: https://docs.divio.com/en/latest/background/project-creation-options#project-creation-platform

..  _multisite-mirrors:

How to create a multi-site Django project using Mirrors
=======================================================

Start with the *original*, the project from which the mirrors will be created. The mirrors will share the codebase,
database and media storage of the original, but will run as wholly independent Docker instances.


Create the mirrors
------------------

Ensure that both Test and Live servers have been successfully deployed.

:ref:`Create one or more mirrors <user:how-to-duplicate-project-options>`.


Apply environment variables to each mirror
--------------------------------------------

Database and media storage
~~~~~~~~~~~~~~~~~~~~~~~~~~

The following environment variables from the Test and Live environments of the original will need to be applied to
the corresponding environments on each of the mirrors:

* ``DATABASE_URL``
* ``DEFAULT_STORAGE_DSN``

You can do this locally, using:

..  code-block:: bash

    divio project env-vars -s test --all   # use live to collect the values from the live server

or you can SSH into the cloud servers and run the ``env`` command to list them.

Using the Control Panel, add the variables to the Test and Live environments of each mirror.


SITE_ID
~~~~~~~

The ``SITE_ID`` of the original will be ``1`` by default. For each mirror, add a ``SITE_ID`` environment variable,
incrementing it each time.

If two sites share the same ``SITE_ID``, or if you save an object in the *Sites* admin before deploying a mirror
with its ``SITE_ID`` in place, you may have unexpected results.


Deploy your mirrors
-------------------

Mirrors can be deployed from their own Dashboards, or from the *Mirrors* view of the original.

In the Django *Sites* admin you will see each mirror now listed.

If you're using a Django application that makes use of the Sites framework, such as django CMS, you will see that
it now has access to multiple independent sites. In django CMS for example this means that pages can be one site of
the project or another.


Managing database migrations
----------------------------

Typically when working with mirrors, code changes will be applied to the original and then rolled out to each
mirror over a period of time - at any rate, not all mirrors will immediately be deployed along with the original.
Because the deployment of any one of the sites will run any outstanding migrations in the database they all share,
this means that you could be in a situation where the database and codebase are out of synchronisation for some of
the sites.


Backwards-compatible migrations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One solution to this is to adopt a two-step strategy for migrations that could be affected.

For example, suppose that a code change removes a database field. In that case, when the original is
deployed, it will immediately change the database schema, and any code in the mirrors that expects to find the
field will fail.

Instead, you would need to:

#. without changing the model field, remove code in views, model methods and so on that would attempt to use the
   field
#. roll out the change to all mirrors
#. remove the field
#. migrate the database

