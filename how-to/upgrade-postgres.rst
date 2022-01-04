.. _how-to-upgrade-postgres:

How to manually upgrade PostgreSQL
==================================

Manual upgrade steps
--------------------

To upgrade your PostgreSQL service instance from one version to another, without any downtime, the following steps 
should be applied to each environment where the upgrade is required. 

1. Check the prefix of the current installation. This will be ``DEFAULT`` if it has not been manually changed. 
2. Add the PostgreSQL service for the new version to your environment. Assign this the default prefix ``NEW``.
3. Deploy the environment(s). 

At this point, the environment is still running on the old version of the database, but the service for the new
version is deployed and ready to receive data. The following steps will copy the data from the existing database to the new 
version. 

4. Create a backup for the ``DEFAULT`` database service. 
5. Restore this backup to the ``NEW`` service.
6. Rename the prefix for the old database version from ``DEFAULT`` to ``OLD``.
7. Detatch the ``OLD`` database service.
8. Rename the prefix for the new database version from ``NEW`` to ``DEFAULT``.
9. Deploy the environment(s).

Your environment is now using the new PostgreSQL service for the upgraded version. 

Risks
-----

As with all database migrations, there is a small risk here. Any data written to the database in the short time between step 4 
(creating the backup of the old database service), and step 9 (deploying the changes) will be lost.

It is the user's responsibility to assess this risk and act accordingly. If your application rarely writes the database and
is mostly reading it, the risk is low. If the only database writes are controlled by you as a Divio user, then this process is safe. 
If, on the other hand, the users of your application are continually creating new records in the database, this process carries a 
higher risk. 

To mitigate this risk, create a :ref:`maintenance window <maintenance>` for the application . During this window your 
application will be offline to users and there will be no risk of data loss. 
