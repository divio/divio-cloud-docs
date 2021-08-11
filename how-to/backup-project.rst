.. _how-to-backup-project:

How to use our backup system
============================

..  seealso::

    :ref:`Divio backup system <knowledge-project-backups>`

The *Backups* view of your project shows the Scheduled and On-demand backups that have been created.

The list of backups shows what was backed up and when, with additional information and options to restore or download
the backup, or create new backups on-demand.


How to create backups
---------------------

* **Scheduled backups** are made according to the project's backup schedule, and require no intervention from the user.

* **On-demand backups** can be made whenever you require.


To create a backup, from the *Backups* view of your project,

* select *Create backup* for the server you want to backup
* choose what to backup: *database*, *media* or both
* hit **Create backup** (you may add a note to the backup)


How to work with existing backups
---------------------------------

Select a particular backup to view more detailed information about it. More importantly, each backup has

* a *Restore* option
* an *options menu*, for further actions, such as *Prepare download*.


The Restore option
~~~~~~~~~~~~~~~~~~

The Restore functionality gives you flexibility. You can choose what to restore (database or media) and its destination
(project and environment).

..  warning::

    A restore operation will overwrite content at the destination. Take a backup before restoring unless you are sure
    you will no longer need that content.


The Download option
~~~~~~~~~~~~~~~~~~~

To download a backup to your own computer, select *Prepare download* from the action menu and choose the content you
want to download. The files will be prepared asynchronously, and an email message containing links to the database
and/or media files will be sent to you when they are ready.

The database will be made available in the form of a database dump

The media files will be made available as a tarred archive, and will include a manifest file listing contents.
