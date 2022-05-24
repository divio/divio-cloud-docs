Local configuration using ``.env-local``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you will see above, the ``web`` service refers to an ``env_file`` containing the environment variables that will be
used in the local development environment.

Divio cloud applications include :ref:`a number of environment variables as standard <env-var-list>`. In addition,
:ref:`user-supplied variables <environment-variables>` may be applied per-environment.

If the application refers to its environment for variables to configure database, storage or other services, it will
need to find those variables even when running locally. On the cloud, the variables will provide configuration details
for our database clusters, or media storage services. Clearly, you don't have a database cluster or S3 instance running
on your own computer, but Docker Compose can provide a suitable database running locally, and you can use local file
storage while developing.

Create a ``.env-local`` file. In this you need to provide some environment variables that are suitable for the
local environment. The example below assumes that your application will be looking for environment variables to
configure its access to a Postgres or MySQL database, and for local file storage: