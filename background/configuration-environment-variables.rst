..  Do not change this document name
    Referred to by: tutorial message 149 project-envvars-info
    Where: in the Environment variables view
    As: https://docs.divio.com/en/latest/background/configuration-environment-variables


.. _environment-variables:

Environment variables
=====================

Divio projects allow you to maintain separate configuration for each of
the *Live*, *Test* and *Local* environments.

Environment variables are dynamic values that can be used by the processes or
applications running on the server. One of the advantages in using them is that
you can isolate specific values from your codebase.

Environment variables are a good place for storing instance-specific
configuration, such as settings that you don't wish to hard-code into
your project.


Cloud (*Live* and *Test*) environments
--------------------------------------

On Cloud sites, environment variables for a project are managed via the command
line, or via the Control Panel. The variables for the *Live* and *Test* sites
are wholly independent.

..  note:

    When you duplicate a project on the Control Panel, its environment
    variables will **not** be copied to the new project. This is intentional,
    as they could include sensitive data, such as API keys.

    The best way to copy environment variables from one project to another is
    by using ``divio project env-vars`` on the command-line to copy (with the
    ``--json`` option for export) and then apply them.


Via the command line
~~~~~~~~~~~~~~~~~~~~

The :ref:`Divio CLI <divio-cli-ref>` allows you to set and check values from
the command line with the ``divio project env-vars`` command, as long as you
are within the path of the local version of the project. For example, to see
the variables of the *Live* server:

..  code-block:: bash

    divio project env-vars -s live

If any exist, they will be displayed thus::

    Key                  Value
    -------------------  -------
    SECURE_SSL_REDIRECT  True

See the :ref:`divio project env-vars <divio-project-env-vars>` reference for
more.


Via the Control Panel
~~~~~~~~~~~~~~~~~~~~~

In the project, select *Environment Variables*. Enter the keys and values, and
**Save**.

.. image:: /images/control-panel-environment-variables.png
   :alt: 'Managing environment variables'


.. _local-environment-variables:

Local environment
-----------------

Your local site also uses environment variables, contained in the
``.env-local`` file.

By default these are::

    DEBUG=True
    STAGE=local
    DATABASE_URL=postgres://postgres@postgres:5432/db


Formatting
~~~~~~~~~~

Lines should not contain spaces or quotation marks (see `Docker's documentation
<https://docs.docker.com/compose/env-file/>`_).


.. _environment-variables-settings:

Environment variables and Django settings
-----------------------------------------

As you can see from the local environment examples above, environment variables
can also be used to apply Django settings, such as ``DEBUG``.

To access the environment variable in your own Python code, you could use
something like this::

    import os
    my_variable = os.environ.get('MY_ENVIRONMENT_VARIABLE')

It's important to note that if your variable represents anything other than a
string, you will need to interpret the variable appropriately, as
``os.environ.get`` will only return a string.

You can also use ``env()`` (from the ``getenv`` package), which will parse the
variable as Python code.


Where and when environment variables are applied
------------------------------------------------

Environment variables should apply only to *environments*, and not to states or processes that are
independent of a particular environment.

* **When a project is running**, it runs in a particular environment, so you can expect environment
  variables to apply.

* **When a project is being built** (i.e. in the deployment phase), it should not be subject to any
  particular environment conditions. Even Django operations that take place during deployment (such
  as ``collectstatic``) should be environment-agnostic - under *all* environment conditions, you
  should expect the same result from ``collectstatic``.

  However you can :ref:`set environment variables during the build phase <setting-env-vars-build>`.


Commonly-used environment variables
-----------------------------------

Many of the applications packaged for Divio deployment recognise a number
of environment variables for your convenience.

See :ref:`key-addons` for lists of settings that can be provided as variables
in some Divio addons.

They do this in their :ref:`configure-with-aldryn-config` files. To see
precisely how they are handled, refer to the ``aldryn_config.py`` file of key
addons (*important*: make sure you are looking at the correct *version* of the
addon, as different versions of the packages will assume different variables
and settings):

Our uWSGI application gateway also :ref:`recognises environment variables
<uwsgi-configuration>` that commence ``UWSGI_``.
