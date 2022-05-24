..  This include is used by:

    * aldryn-django-02-create-project.rst
    * laravel-02-create-project.rst
    * wagtail-02-create-project.rst


About deployment
-------------------------

Any time new changes to the application code are committed to its repository, the Control Panel will indicate this with a
message showing the number of undeployed commits for each of its server environments.

.. image:: /images/intro-dashboard-commits.png
   :alt: 'Deployed and undeployed commits'
   :class: 'main-visual'

New code and configuration changes applied via the Control Panel (to subscriptions, cron jobs, environment variable,
domains or other settings) will not take effect on either server environment until it is deployed once again.

If for whatever reason a deployment fails, there will be no down-time - the containers that are currently running will
continue running, and the failing changes will not be deployed.


Explore the Dashboard
---------------------

The Divio application Dashboard provides you with access to useful controls and information for the application. They 
are fairly self-explanatory and at this stage you don't need to interact with any of them, but it's worth familiarising
yourself with what's available.

Enable Beta options
~~~~~~~~~~~~~~~~~~~

We often expose new functionality to users who opt-in to Beta features. You can do this in your `account settings
<https://control.divio.com/account/contact/>`_.
