..  This include is used by:

    * django-02-create-project.rst
    * laravel-02-create-project.rst
    * wagtail-02-create-project.rst


The new project doesn't do anything very useful or interesting yet - but it's up and running and ready to start working
on.


About deployment
-------------------------

Any time new changes to the project code are committed to its repository, the Control Panel will indicate this with a
message showing the number of undeployed commits for each of its server environments.

New code and configuration changes applied via the Control Panel (to subscriptions, cron jobs, environment variable,
domains or other settings) will not take effect on either server environment until it is deployed once again.

If for whatever reason a deployment fails, there will be no down-time - the containers that are currently running will
continue running, and the failing changes will not be deployed.


Explore the Dashboard
---------------------

The Divio project Dashboard provides you with access to useful controls and information for the project. They are
fairly self-explanatory and at this stage you don't need to interact with any of them, but it's worth familiarising
yourself with what's available.
