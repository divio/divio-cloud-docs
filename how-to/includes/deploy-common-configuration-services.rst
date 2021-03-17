Configuring your application
----------------------------------------------

Your application will require configuration. You may be used to hard-coding such values in the application itself -
though you can do this on Divio, **we recommend not doing it**. Instead, all application configuration (for access to
services such as the database, security settings, etc) should be managed via environment variables.

Divio provides services such as database and media. To access them, your application will need the credentials. For
each service in each environment, we provide an :ref:`environment variable <environment-variables>` containing the
values required to access it. This variable is in the form:

..  code-block:: text

    schema://<user name>:<password>@<address>:<port>/<name>

Your application should:

* read the variables
* parse them to obtain the various credentials they contain
* configure its access to services using those credentials

We also provide environment variables for things like security configuration.
