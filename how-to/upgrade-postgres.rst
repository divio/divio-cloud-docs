.. _how-to-upgrade-postgres:

How to manually upgrade PostgreSQL
==================================

Manual upgrade steps
--------------------

To upgrade your PostgreSQL service instance from one version to another, without any downtime, the following steps 
should be applied to each environment where the upgrade is required. Note that for these instructions to be valid there
will be more than one PostgreSQL service availabe. Ensure you select the correct versions when provisioning and deprovisioning
the "old" and "new" versions of your PostgreSQL service.

1. Check the prefix of the current installation. This will be ``DEFAULT`` if it has not been manually changed, but can be anything. 
   For the purposes of these instructions we will refer to it as ``DEFAULT``.

..  image:: /images/postgres-upgrade-existing-service.png
    :alt: 'Existing PostgreSQL service with prefix "DEFAULT"'
    :class: 'main-visual'

2. Add the PostgreSQL service for the new version to your environment. Assign this the default prefix ``NEW``.

..  image:: /images/postgres-upgrade-add-new-service.png
    :alt: 'Add the new PostgreSQL service with prefix "NEW"'
    :class: 'main-visual'

3. Provision the new PosgreSQL service. 

..  image:: /images/postgres-upgrade-provision-new-service.png
    :alt: 'Provision the new version of the PostgreSQL service'
    :class: 'main-visual'

4. Repeat steps 1-3 for each environment.

At this point, the environment is still running on the old version of the database, but the service for the new
version is deployed and ready to receive data. The following steps will copy the data from the existing database to the new 
version. 

.. note:: When a service shows as ``Attached``, it means that it is ready to use. It does not indicate that it is being used by 
    your environment. The new version will not be in use until you deploy the changes in step 11.

    For more information on how and when services are provisioned and attached, please see the Services documentation: https://docs.divio.com/en/latest/background/services/

5. Create a backup for the ``DEFAULT`` database service. 

..  image:: /images/postgres-upgrade-backup-default.png
    :alt: 'Backup the old version of the PosgreSQL service'
    :class: 'main-visual'

..  image:: /images/postgres-upgrade-backup-default2.png
    :alt: 'Backup information after completion'
    :class: 'main-visual'

6. (Optional) Prepare a backup download and back this up somewhere. This step is not required from a migration perspective, but 
   may be needed to comply with local policies or just useful as a pre-migration snapshot later.

7. Once the backup has completed, restore it to the ``NEW`` service.

..  image:: /images/postgres-upgrade-restore-backup-to-new.png
    :alt: 'Restore the old backup to the new PostgrSQL service'
    :class: 'main-visual'

8. Rename the prefix for the old database version from ``DEFAULT`` to ``OLD``.
9.  Detach the ``OLD`` PostgreSQL service.

..  image:: /images/postgres-upgrade-detach-old-service.png
    :alt: 'Detach the old PostgreSQL service'
    :class: 'main-visual'

10. Rename the prefix for the new database version from ``NEW`` to ``DEFAULT`` (or whatever prefix your original PostgreSQL service
    had prior to the upgrade).
11. Deploy the environment.
12. Delete the ``OLD`` PostgreSQL service.

..  image:: /images/postgres-upgrade-delete-old-service.png
    :alt: 'Delete the old PostgreSQL service'
    :class: 'main-visual'

13. Repeat steps 5-11 for each environment.

Your environment is now using the new PostgreSQL service for the upgraded version. 

In order to run the application locally with the upgraded database, a few extra steps are required:

14. Update ``docker-compose.yml`` for the application to use the PostgrSQL image ``postgres:13.5-alpine``.
15. Run ``docker-compose down -v`` to stop the containers and remove the volumes.
16. Run ``divio app pull db <environment>`` to pull the updated database from the environment you want locally. 
17. Run ``docker-compose up`` to bring everything up again. 

Risks
-----

As with all database migrations, there is a small risk here. Any data written to the database in the short time between step 4 
(creating the backup of the old database service), and step 9 (deploying the changes) will be lost.

It is the user's responsibility to assess this risk and act accordingly. If your application rarely writes the database and
is mostly reading it, the risk is low. If the only database writes are controlled by you as a Divio user, then this process is safe. 
If, on the other hand, the users of your application are continually creating new records in the database, this process carries a 
higher risk. 

To mitigate this risk, ensure that your application (or any parts of it that write to the database) is unreachable during the period that these operations are being performed. 
