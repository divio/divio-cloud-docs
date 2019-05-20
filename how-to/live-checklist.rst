..  _live-checklist:

Go-live checklist
================================

Check your subscription plan
----------------------------

* In the Control Panel, check the project's *Subscription*, and that it includes the technical and
  support resources it will require once the site is live.


Dependencies
------------

* Consider :ref:`pinning all dependencies <manage-dependencies>`. This will help ensure that future
  deployments do not introduce unexpected software updates.


``DEBUG`` mode
--------------

* Ensure that your Live server is configured to run with ``DEBUG = False`` (this is the default,
  but may have been changed during development).


Domains
-------

* If you are using existing domains, prepare them for the switch. Ensure that they have low (less than 60 seconds)
  TTLs. High TTLs can cause problems when the domains are pointed at the new site, including delays in the automatic
  provisioning of SSL certificates.
* Check that the live domain for the server is set up for the site in the Control Panel (support article: `how to use
  your own domain with Divio Cloud
  <http://support.divio.com/control-panel/projects/how-to-use-your-own-domain-with-divio-cloud>`_).
* Check that any domains that should redirect to the primary domain are also set in the *Domains* setting in the
  Control Panel.
* If required, enable redirects to HTTPS by setting the :ref:`SECURE_SSL_REDIRECT environment variable
  <security-middleware-settings>` to ``True``.


Environment variables
---------------------

* Check that any other environment variables required on Live have been set (support article: `How
  to use environment variables with your projects
  <http://support.divio.com/control-panel/projects/how-to-use-environment-variables-with-your-projec
  ts>`_).


Serving configuration
---------------------

* Check the Aldryn Django addon configuration. We recommend the :ref:`Hash static filenames
  <hash-static-file-names>` option, which lets you take advantage of caching.


Other settings
--------------

* Check your project's ``settings.py`` for any settings that may have been temporarily configured
  during development.


Deployment
----------

* Run a deployment of the Live server. If you have been using the Test server to build content
  prior to launch, us the *Copy data from Test and deploy* option.


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
