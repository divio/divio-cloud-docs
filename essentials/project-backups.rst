.. _knowledge-project-backups:

Divio project backups
=====================

..  seealso::

    :ref:`How to backup your projects <how-to-backup-project>`.

Our backup system is designed with pragmatic, real-world needs and concerns in mind.

Backups on Divio are in accordance with two key principles.

* Data integrity - the integrity of your data and content is paramount, and they must be kept safe.
* Portability - your project belongs to you. Your data and content must be as portable as possible, so that you can sign
  up to our services confident that you will never find yourself locked in to them.


What’s backed up?
-----------------

Our backup system takes care of your applications’s:

* database - the database that Django uses for persistent storage, made available for download as a binary database dump
* media files - files uploaded/processed/stored by the project’s applications, made available for download as a tarred
  archive, and including a manifest file of contents

Your backups are made to encrypted storage.

..  note::

    Your applications’s codebase is not captured in our backups, as it already versioned in Git.


Backup storage
-----------------------

Backups in AWS-based regions are stored in the same region as the application using AWS S3 `Standard-IA storage class
<https://aws.amazon.com/s3/storage-classes/>`_.

This storage class stores data redundantly across multiple datacenters called `availability zones
<https://aws.amazon.com/about-aws/global-infrastructure/regions_az/>`_ in the same region. Availability zones give
customers the ability to operate production applications and databases that are highly available, fault tolerant,
and scalable. All traffic between availability zones is encrypted.


Scheduled and on-demand backups
-------------------------------

Backups are initiated in two different ways:

* on-demand - when the user requests it
* scheduled - according to a schedule determined by the project's subscription


Retention policies
------------------

On-demand backups
~~~~~~~~~~~~~~~~~

Various policies are available, but in all environments this is set by default to a 30 days/3 backups policy, meaning
that these backups will be retained indefinitely; however, of those that are more than 30 days old, only the three most
recent will be retained.


Scheduled backups
~~~~~~~~~~~~~~~~~

Various policies are available but in all environments this is set by default to a 7-daily/4-weekly/12-monthly
*grandfather-father-son* policy. This means that:

* Each day, the system will take a backup, and discard any daily backups older than seven days.
* Each week, it will relabel the oldest daily backup as a weekly backup and discard any weekly backups older than one
  month.
* Each month, it will relabel the oldest weekly backup as a monthly backup and discard any monthly backups older than
  one year.

After a year, the system will have retained:

* twelve monthly backups spanning the last year
* four weekly backups spanning the last month
* seven daily backups spanning the last week
