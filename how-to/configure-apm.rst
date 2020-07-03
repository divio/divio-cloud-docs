.. _configure-apm:

How to configure Application Performance Monitoring
===================================================

This example uses Elastic APM in a Django project. However, the principles are the same for other projects and services.


Set up the APM instance
-----------------------

Log in via the `Elastic control panel <https://cloud.elastic.co>`_.

Create a new Elastic deployment. It makes sense to select the same cloud platform and region you're using on Divio -
select *AWS US East* unless you know otherwise, and the default *I/O Optimized* configuration.

Note the *username* and *password* provided for future reference. The APM instance created will also have a *secret
token*; make a note of this too. Finally, you will need to copy the *APM Server URL*. (It takes a few moments to create
and the instance and for all this information to become available.)

Other services will allow you to create an instance and will provide the credentials for using it in much the same way.


Install and configure the Divio Telemetry addon
-----------------------------------------------

`Divio Telemetry <https://github.com/divio/divio-telemetry-apm>`_ is available as an Aldryn addon via the Control
Panel. It uses the official `elastic-apm <https://pypi.org/project/elastic-apm/>`_ package provided by Elastic, and adds easy configuration via a single environment variable, ``DEFAULT_APM_DSN``.

..  note::

    At the time of writing, you will need to pin the ``elastic-apm`` package in your ``requirements.in``::

        elastic-apm<5.8.0

    as the result of a `known issue <https://github.com/elastic/apm-agent-python/issues/880>`_.

``DEFAULT_APM_DSN`` is a URL, and can be assembled from the Elastic credentials you collected earlier. It's in the
form::

  https://<Divio project slug>:<secret token>@<APM Server URL>:443

Your own URL should look something like::

  https://apm-elastic-test:lAGtsyPGvg2T4o25Yr@d26758984b0c7792826e42918c785738.apm.us-east-1.aws.cloud.es.io:443

It should **not** include the protocol fragment (``https://``) of the APM Server URL.

Apply this as an environment variable, either using the Control Panel, or in the ``.env-local`` file. It makes sense
to use a different APM instance for each environment.

Using a different provider, you will need to install the appropriate software in your project and provide it with the
necessary credentials to access the third-party service.


Check the results
-----------------

When the project has been rebuilt/deployed as required, you can visit the APM Server URL. Log in with the username and
password. Your new instance will be displayed, along with the data it has collected.
