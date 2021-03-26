..  This include is used by:

    * deploy-django.rst
    * django-deploy-quickstart.rst

Deploy the Test server
~~~~~~~~~~~~~~~~~~~~~~

Deploy with:

..  code-block:: bash

    divio project deploy

(or use the **Deploy** button in the Control Panel).

Once deployed, your project will be accessible via the Test server URL shown in the Control Panel (append ``/admin``),
but note that you won't be able to log in until you complete the next step.


Working with the database on the cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your cloud project does not yet have any content in the database, so you can't log in or do any other work there.
You can push the local database with the superuser you created to the Test environment:

..  code-block:: bash

    divio project push db

or, use the ``divio project ssh`` command to open a shell in the Test environment. There you can execute Django
migrations and create a superuser in the usual way.

Optionally, but recommended, you can run migrations automatically on deployment by adding a :ref:`release command
<release-commands>` in the Control Panel.
