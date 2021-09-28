.. _manage-environment-variables:

How to manage your application's environment variables
========================================================

Your project relies on environment variables to configure application settings and access to
storage, database and other services.

Environment variables can be set independently for each environment, whether on the cloud or
locally.

Environment variables can be set:

* automatically by our infrastructure (particularly for key services, such as the database)
* by the user, either to add new variables or overwrite ones set by the system

..  seealso::

    * :ref:`Environment variables reference <environment-variables>`


.. _reading-env-vars:

Reading environment variables
-----------------------------

From cloud environments
~~~~~~~~~~~~~~~~~~~~~~~~

Using the Divio CLI
^^^^^^^^^^^^^^^^^^^

To read custom variables from the default cloud environment:

..  code-block:: bash

    divio project env-vars

From another environment, using the ``-s`` option:

..  code-block:: bash

    divio project env-vars -s live

Use the ``--all`` flag to include automatically applied variables, for example:

..  code-block:: bash

    ➜ divio project env-vars -s live --all

    Key               Value
    ----------------  -----------------------------------------------------------------------------------------------------------------------------------------------------------------
    ALT_DATABASE_DSN      mysql://example:Ro1T-d4Ldeaddeadqu6Gu3tkIt@appctl-black-mysql-00.cluster-cs4nfpsgul9fcn.us-east-1.rds.amazonaws.com:3306/example-live-b00bde685-deade65
    CACHE_URL             db://django_dbcache
    DEBUG                 False
    DEFAULT_DATABASE_DSN  postgres://example-live-bead1e173ef383-3638:OIut5vYvWjI3UQzcAGJ4aJIXGWBTscsq_MobDltHiUMiI2VHFbxyW_yKYAl5-aw0F@appctl-black-sites-02.cs4nx9fcn.us-east-1.rds.amazonaws.com:5432/example-live-bead1e173ef3833638-ee6263
    DEFAULT_STORAGE_DSN   s3://A5JHDYDTYZ3PLOF:t62LdAvROXgFR14%2BOwidSI6N9WQL454G0ipJY@example-live-b328dddd68536e314797994491-c967f23.divio-media.org.s3.amazonaws.com/?auth=s3v4&domain=example-live-b32868536e314797994491-c967f23.divio-media.org
    DOMAIN                example.us.aldryn.io
    DOMAIN_ALIASES        .*
    GIT_BRANCH            master
    SECRET_KEY            AX1Rxxxxxxwdm1klEQOPukngZFO58vbbpeqp5l0ogdRspdKZTuutJ5V2ov
    SITE_NAME             example.
    STAGE                 live
    TEMPLATE_DEBUG        False
    example_url           https://www.example.com



See the :ref:`divio-cli-command-ref` reference for further information.


Using the Control Panel
^^^^^^^^^^^^^^^^^^^^^^^

Use the *Env Variables* view of a project to view (and add) custom variables.


In a terminal session to a cloud container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``env`` command will list all variables.


Setting environment variables
------------------------------------

Setting a custom variable with the same name as one specified by the system will overwrite it.

..  important::

    In all cases, changes to environment variables will not apply until the environment is
    relaunched (redeployed on the cloud, or restarted locally).


In cloud environments
~~~~~~~~~~~~~~~~~~~~~

Using the Divio CLI
^^^^^^^^^^^^^^^^^^^

Use ``divio project env-vars --set``, for example to target the default environment:

..  code-block:: bash

    divio project env-vars --set example_url https://www.example.com

or to specify an environment with the ``-s`` option:

..  code-block:: bash

    divio project env-vars -s live --set example_url https://www.example.com

See the :ref:`divio-cli-command-ref` reference for further information.


Using the Control Panel
^^^^^^^^^^^^^^^^^^^^^^^

Use the *Env Variables* view of a project to view and add custom variables. Variables need to be
configured for each environment.

.. _env-var-port:

``PORT`` environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the load-balancer is unable to connect to the environment's of the application within reasonable time, the runtime
logs should contain information such as a traceback revealing a programming error, a *\[busyness\]* that the application
was too slow to start up or a port number was not auto detected. If you suspect that, the exposed port is not correctly
detected, you can configure a ``PORT`` environment variable, for example ``8000``, to manually set the port number.


Leading and trailing spaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Control Panel does not strip leading or trailing spaces from values. Be careful when pasting in values that you do
not inadvertently include unwanted spaces.

If you get an unexpected error in your logs that includes a reference to an environment variable value with a ``%20``
character in it - that's a sure sign that it probably includes an undesired space.


In the local environment
~~~~~~~~~~~~~~~~~~~~~~~~

By default, the ``.env-local`` file is used to store variables for the local environment (as
specified by the ``env_file: .env-local`` in the ``docker-compose.yml`` file).


.. _setting-env-vars-build:

In the build phase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``ENV`` in the ``Dockerfile`` to set an environment variable that will be used for the rest of the build process,
and will also be baked into the image and accessible at runtime.

..  code-block:: dockerfile

    ENV <key>=<value>

You can also force a particular command to run with a certain environment variable:

..  code-block:: dockerfile

    RUN <key>=<value> <command>

However, the environment variables with which the cloud environments are provisioned (for example, for services such as
database and media storage) are not accessible at build time (nor would it be desirable to rely on them in the build,
since the same image will be used in multiple cloud environments).
