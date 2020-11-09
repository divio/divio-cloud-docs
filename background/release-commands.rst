..  Do not change this document name
    Referred to by: https://control.divio.com/admin/tutorial/message/147/change/
    Where: in the Settings view
    As: https://docs.divio.com/en/latest/background/release-commands


.. _release-commands:

Release commands (Beta)
=========================

..  note::

    Release commands are currently provided as a Beta feature, and are available only to users who have signed up for
    access to Beta-release features. `Enable Beta features in your account settings
    <https://control.divio.com/account/contact/>`_.


What are release commands?
--------------------------

*Release commands* are executed during the deployment process, in a container launched from the application's image.
After all the release commands have been performed, the container is discarded and the deployment process continues.

Release command are suited to performing actions that take place *in* the application's runtime environment. For
example, actions such as:

* running database migrations (e.g. ``python manage.py migrate`` in Django)
* programmatically applying headers to media storage
* performing a self-test or batch repair on an application's content (e.g. ``python manage.py cms fix-tree`` in django
  CMS)
* performing a self-test on an application's configuration
* using an API hook to flush a content cache
* posting a notice to a company messaging tool to announce a successful deployment

are all good examples of release commands.

They are to be contrasted with actions that take place *during the build process* to define the application's runtime
environment - for example, compilation of language files or static files - that should be executed in the
``Dockerfile``.

If a release command fails or raises an error, the deployment will fail.


Applying release commands
-------------------------

Release commands can be added in a project's *Settings* view, along with a human-readable label.

.. image:: /images/release-commands.png
   :alt: 'Release commands'
   :class: 'main-visual'

Commands will be executed in the order that they are added.

Commands can also be added programmatically by applications - for example those that use the Aldryn Django framework -
and will be listed here as well.


Cautions
--------

Risk of failed automated commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Release commands are executed in the runtime environment, and therefore have access to an application's resources and
services. This includes the database and media storage. For example, a database migration in a release command can
alter the structure of the database.

Even if a release command is completed successfully, it is not the final stage in the deployment process, and
subsequent checks can also fail, in which case the new image will not be used; instead, the containers launched at the
previous deployment will continue running, potentially putting the application into an inconsistent state.

Mitigations such as implementing roll-back mechanisms are the responsibility of the application developer.


Timeouts
~~~~~~~~

Release commands are suitable for running long-executing processes (for example, S3 header updates can take some time
to execute) so we apply a generous timeout (30 minutes). However, commands that exceed this limit will cause a
deployment failure.


Failures
--------

On deployment, a release command that produces an error will be shown in the deployment log under the ``docker migrate
release`` heading, for example:

..  code-block:: text

    ===== docker release commands =====

    Running security configuration checks...

    database configuration    ... passed
    user accounts             ... passed
    gateway server            ... failed (HTTPS not enforced; no exemptions)

    Security configuration checks failed.
