.. _deploy:

Deploy your application to Divio
=================================

The steps outlined here assume that you have already:

* built a suitable application in Docker and prepared it for deployment (see :ref:`Configure an existing web
  application for deployment <how-to-existing-web-application>` or :ref:`Create a new application
  <how-to-use-quickstart>`)
* set up the :ref:`local development environment <local-cli>`


.. _deploy-create-new-project:

Create a new project on Divio
--------------------------------------------

The first step is to create a project on the Divio Control Panel, with your application repository. There are two ways
of doing this:

* *New project*, in which you will push your local Git code to Divio's Git server
* *New project from Git repository* (Beta), in which your Divio project will fetch the code from a Git host

..  image:: /images/new-project.png
    :alt: 'New project options'
    :width: 327


Creating a new project
~~~~~~~~~~~~~~~~~~~~~~

In the Divio Control Panel, add a `New project <https://control.divio.com/control/project/create/>`_. Select the
*Build your own* option.


Creating a new project from a Git repository (Beta)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Divio Control Panel, add a `New project from Git repository
<https://control.divio.com/control/project/import/>`_. Once you have supplied the Git repository URL, you will need
to use the public key provided to create a Deploy Key on the repository.

You should also :ref:`add a webhook <git-setup-webhook>`, so that when new commits are pushed to the repository, it
will send a signal to update the Divio Control Panel.

..  admonition:: Beta status limitations

    Creating a new project from a Git repository is currently provided as a Beta feature, and is available only to
    users who have signed up for access to Beta-release features. `Enable Beta features in your account settings
    <https://control.divio.com/account/contact/>`_.

    Some limitations apply to the current version of this functionality. In order to import a repository, at the
    time of import:

    * you will need to enable write access on the repository's deploy key
    * the repository will need a ``master`` branch

    Once imported, you can remove the write access and can delete the ``master`` branch if you don't need it.


Connect your local application to the cloud project
------------------------------------------------------------------

Connecting a local application to a Divio project on the cloud allows you to interact with and
manage the cloud project from your command-line.

The cloud project has a *slug*, based on the name you gave it when you created it. Run:

..  code-block:: bash

    divio project list -g

to get your project's slug.

You can also get the slug from the Control Panel:

..  image:: /images/intro-slug.png
    :alt: 'Project slug'
    :width: 483

Run:

..  code-block:: bash

    divio project configure

and provide the slug. (``divio project configure`` creates a new file in the project at ``.divio/config.json``,
containing the configuration data.)


Configure Git (if required)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using Divio's own Git server for this project rather than an external Git provider, add the project's Git
repository as a remote, for example:

..  code-block:: bash

    git remote add divio git@git.divio.com:my-divio-project.git

The Git URL is provided by the ``divio project configure`` command above, and in the *Repository* view of the Control
Panel.


Add database and media services
--------------------------------------------

The new Divio application does not include any :ref:`additional services <services>`. If your application requires a
database or media store, they must be added manually using the Divio Control Panel as required. Use the *Services* menu
to add the services your application needs.


Add release commands
----------------------

If your application needs to perform operations each time it is deployed, for example start-up health tests or
database migrations, these should be applied as :ref:`release commands <release-commands>`.


Add additional environment variables
--------------------------------------------

Your application may require additional environment variables in production. Apply any environment variables using the
Divio Control Panel or CLI.


Push local database/media content
--------------------------------------------

If you have local database or media content, push them to the Test environment:

..  code-block:: bash

    divio project push db
    divio project push media

See also :ref:`Divio CLI usage examples <local-cli-usage>`.


Push your code
--------------

Push your code to the Git repository, whether on Divio's own Git server or hosted with an external Git provider.

Set the Git branch appropriately for each of your :ref:`cloud environments <environments>`.


Deploy the Test server
----------------------

Deploy with:

..  code-block:: bash

    divio project deploy

(or use the **Deploy** button in the Control Panel).

Once deployed, your project will be accessible via the URLs shown in the Control Panel for each environment.

See our :ref:`go-live checklist <live-checklist>` for a production deployment.
