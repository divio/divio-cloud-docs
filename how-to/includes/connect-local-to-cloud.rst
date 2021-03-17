..  This include is used by:

    * how-to/django-deploy-quickstart-common-steps.rst
    * how-to/deploy-generic.rst
    * how-to/deploy-django.rst
    * how-to/deploy-flask.rst

Connect the local project to the cloud project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your Divio project has a *slug*, based on the name you gave it when you created it. Run ``divio project list -g`` to
get your project's slug.

You can also read the slug from the Control Panel:

..  image:: /images/intro-slug.png
    :alt: 'Project slug'
    :width: 483

Run:

..  code-block:: bash

    divio project configure

and provide the slug. This creates a new file in the project at ``.divio/config.json``.

The command also returns the Git remote value for the project. You'll use this in the next step.

Now the local project is connected to the cloud project, ``divio project dashboard`` will open the project in the
Control Panel.
