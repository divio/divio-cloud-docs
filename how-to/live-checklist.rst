..  _live-checklist:

Go-live checklist
================================

Check your subscription plan
----------------------------

In the Control Panel, check the project's *Subscription*, and that it includes the technical and support resources it
will require once the site is live.


Dependencies
------------

Pin all dependencies in the project, so that future deployments do not introduce unexpected software updates.

* **Python applications**: see :ref:`pinning all dependencies in Python applications <manage-dependencies>`.


Turn off developement mode
----------------------------------------

Many frameworks include a development mode that exposes additional information. This should not go into production.

* **Django applications**: this is handled by the ``DEBUG`` setting. When using our :ref:`recommended Django project
  configurations <working-with-recommended-django-configuration>`, this will be handled correctly automatically.


Domains
-------

* If you are using existing domains, prepare them for the switch. Ensure that they have low (less than 60 seconds)
  TTLs. High TTLs can cause problems when the domains are pointed at the new site, including delays in the automatic
  provisioning of SSL certificates.
* Check that the live domain for the server is set up for the site in the Control Panel.
* Check that any domains that should redirect to the primary domain are also set in the *Domains* setting in the
  Control Panel.


HTTPS
-----

Set your application to redirect to HTTPS.

* **Django**: :ref:`Django projects using our recommended configuration
  <working-with-recommended-django-configuration>`, will be apply redirects to HTTPS by default.
* **Legacy Aldryn projects**: enable redirects to HTTPS by setting the :ref:`SECURE_SSL_REDIRECT environment
  variable <security-middleware-settings>` to ``True``.
* **Node**: :ref:`how-to-express-js-https`


Environment variables
---------------------

* Check that any other environment variables required on the Live environment have been set (see: :ref:`Environment
  variables <environment-variables>`).


File serving configuration
--------------------------

Check the configuration of static file serving. Files should be appropriately collected, compressed and so on. Hasing
static filenames lets you take advantage of caching.

* **Legacy Aldryn projects**: we recommend using the :ref:`Hash static filenames <hash-static-file-names>` option.


Other settings
--------------

Check your project's configuration for any settings that may have been temporarily configured during development.


Local tests
------------

In the local environment, run the application in a configuration that is as close as possible to the production
configuration. For example, our recommended Docker Compose configurations use development servers for convenience; you
can comment out the ``command`` entry in the ``docker-compose.yml`` file and allow the application to use the
``Dockerfile``'s ``CMD`` instead, which will use a production server.

See :ref:`local-in-live-mode` for more.


Deployment
----------

* If required, copy database and media content to the Live environment.
* Run a deployment of the Live environment.


After deployment
----------------

* Run a crawler on the live site to check for broken links, such as the `W3C Link Checker
  <https://validator.w3.org/checklink>`_ or the open-source `LinkChecker application
  <https://wummel.github.io/linkchecker/>`_.
* Check your site as a logged-in user, an anonymous user and in your browser's private/incognito
  mode to verify expected behaviour.
* Check response times with a tool such `Pingdom <https://tools.pingdom.com>`_.
* If necessary, allocate more resources to the project via its *Subscription* and consult the
  :ref:`live-performance` guide.
