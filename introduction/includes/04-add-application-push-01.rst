..  This include is used by:

    * django-04-add-application.rst
    * wagtail-04-add-application.rst


Using ``divio project push/pull``
---------------------------------

Your local database has new content, but your cloud database hasn't been touched by the work you did locally. One very
useful function of the Divio CLI is ability to push and pull your database and media storage to and from the cloud
environments. For example, try:

..  code-block:: bash

    divio project push db

This will push the local database to the cloud Test environment. Once the process has completed, you can refresh the
cloud Test site; you'll see that it now has the same content in its database as the local site.

Similarly, you can push/pull media files, and also specify which cloud environment. See the :ref:`local commands
cheatsheet <cheatsheet-project-resource-management>`. A common use-case is to pull live content into the development
environment, so that you can test new development with real data.
