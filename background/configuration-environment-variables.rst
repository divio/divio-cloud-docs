..  Do not change this document name
    Referred to by: tutorial message 149 application-envvars-info
    Where: in the Environment variables view
    As: https://docs.divio.com/en/latest/background/configuration-environment-variables


.. _environment-variables:

Environment variables
=====================

Divio applications allow you to maintain separate configuration for each of
the cloud environments as well as the local environment.

Environment variables are a good place for storing instance-specific
configuration, such as settings that you don't wish to hard-code into
your application.


Cloud environments
--------------------------------------

In cloud applications, environment variables can be managed via the command
line or via the Control Panel.

New or changed environment variables are not available to environments until they are redeployed.

Via the command line
~~~~~~~~~~~~~~~~~~~~

The :ref:`Divio CLI <divio-cli-ref>` allows you to set and check values from
the command line with the ``divio app env-vars`` command. For example, to see
the variables of the *Live* server:

..  code-block:: bash

    divio app env-vars --remote-id <numerical application id> -s live

If any exist, they will be displayed thus::

    Key                  Value
    -------------------  -------
    SECURE_SSL_REDIRECT  True

See the :ref:`divio CLI command reference <divio-cli-command-ref>` reference for
more.


Via the Control Panel
~~~~~~~~~~~~~~~~~~~~~

In the application, select *Environment Variables*. Enter the keys and values, and
select **Add**.

.. image:: /images/control-panel-environment-variables.png
   :alt: 'Managing environment variables'


.. _local-environment-variables:

Local environment
-----------------

Your local application also uses environment variables, Docker Compose specifies a file where they can be found, e.g.::

    env_file: .env-local

Lines in the file should not contain spaces or quotation marks (see `Docker's documentation
<https://docs.docker.com/compose/env-file/>`_).


Where and when environment variables are applied
------------------------------------------------

Environment variables should apply only to *environments*, and not to states or processes that are
independent of a particular environment.

* **When an application is running**, it runs in a particular environment, so you can expect environment
  variables to apply.

* **When a application is being built** (i.e. in the deployment phase), it should not be subject to any
  particular environment conditions.

  However you can :ref:`set environment variables during the build phase <setting-env-vars-build>`.


Environment variables with Aldryn (legacy)
-------------------------------------------

Many of the applications packaged for Divio deployment recognise a number
of environment variables for your convenience.

See :ref:`key-addons` for lists of settings that can be provided as variables
in some Divio addons.

They do this in their :ref:`configure-with-aldryn-config` files. To see
precisely how they are handled, refer to the ``aldryn_config.py`` file of key
addons (*important*: make sure you are looking at the correct *version* of the
addon, as different versions of the packages will assume different variables
and settings):

Our uWSGI application gateway in Aldryn Django applications also :ref:`recognises environment variables
<uwsgi-configuration>` that commence ``UWSGI_``.
