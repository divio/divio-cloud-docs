.. _knowledge-zero-downtime:

Zero-downtime deployment system
===============================

Divio allows you to deploy a new version of your site without interrupting service.

When a project environment is deployed with new code, the site will switch from the old deployed version to the new
one without skipping a beat. There is no downtime required while a build takes place. As soon as the newly deployed
containers are available to serve the site, they will take over the application-serving duties.

Each deployment includes multiple self-tests and health-checks, all of which must pass in order for the deployment to
be declared successful. Only then will the new deployment be put into production. If any test fails, the deployment
will fail, but the site will keep running as if nothing had changed.

This allows us to provide zero-downtime deployments - even in cases of *error or failure*.
