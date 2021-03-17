Security settings
~~~~~~~~~~~~~~~~~~~~~~~~~

Typically, an application's security settings will depend upon multiple variables. Some that are typically needed are
provided by Divio's cloud environments. For example, your application is likely to need information about:

* the domains under which the application is served, provided by :ref:`DOMAIN <env-var-domain>` and
  :ref:`DOMAIN_ALIASES <env-var-domain-aliases>`
* a random secret key, provided by :ref:`SECRET_KEY <env-var-secret-key>`

Other variables specific to the application will need to be applied manually for each environment.
