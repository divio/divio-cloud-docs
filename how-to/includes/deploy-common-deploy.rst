Deployment to Divio
--------------------------------------------

Create a new project on Divio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step is to create a project on the Divio Control Panel, with your application repository.

You have two ways of doing this:

..  image:: /images/new-project.png
    :alt: 'New project options'
    :width: 327

* *New project*, in which you will push your local Git code to Divio's Git server
* *New project from Git repository* (Beta), in which your Divio project will fetch the code from a Git host

..  tab:: New project

    In the Divio Control Panel, add a `New project <https://control.divio.com/control/project/create/>`_. Select the
    *Build your own* option.

    Once the project has been created, copy the project's Git URL from its *Repository* view. Add the project's Git
    repository as a remote, for example:

    ..  code-block:: bash

        git remote add divio git@git.divio.com:my-divio-project.git

    Commit and push your work.

    ..  note::

        If you're using the ``master`` branch, you will need to force push to overwrite the initial commits in a Divio
        project with your own.

    You can use ``divio project`` commands such as ``divio project dashboard`` to interact directly with the Divio
    project.


..  tab:: New project from Git repository (Beta)

    In the Divio Control Panel, add a `New project from Git repository
    <https://control.divio.com/control/project/import/>`_. Once you have supplied the Git repository URL, you will need
    to use the public key provided to create a Deploy Key on the repository.

    ..  admonition:: Beta status limitations

        Some limitations apply to the current version of this functionality. In order to import a repository, at the
        time of import:

        * you will need to enable write access on the repository's deploy key
        * the repository will need a ``master`` branch

        Once imported, you can remove the write access and can delete the ``master`` branch if you don't need it.

    You should also :ref:`add a webhook <git-setup-webhook>`, so that when new commits are pushed to the repository, it
    will send a signal to update the Divio Control Panel.

In the *Environments* view, configure each environment to use the appropriate branch.


Connect your local application to the cloud project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can connect a local application to a Divio project on the cloud. This is very convenient, allowing you to interact
with the cloud project from your command-line.

Run:

..  code-block:: bash

    divio project configure

and provide the slug (this creates a new file in the project at ``.divio/config.json``).


The cloud project has a *slug*, based on the name you gave it when you created it. Run ``divio project list -g`` to get
your project's slug.

You can also read the slug from the Control Panel:

..  image:: /images/intro-slug.png
    :alt: 'Project slug'
    :width: 483

You can now use commands such as:

..  code-block:: bash

    divio project dashboard
    divio project pull db  # also push
    divio project pull media  # also push
    divio project deploy

See :ref:`some usage examples <local-cli-usage>`.


Add database and media services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The new Divio application does not include any :ref:`additional services <services>`. If your application requires a
database or media store, they must be added manually using the Divio Control Panel as required. Use the *Services* menu
to add the services your application needs.


Add release commands
~~~~~~~~~~~~~~~~~~~~

If your application needs to perform operations each time it is deployed, for example start-up health tests or
database migrations, these should be applied as :ref:`release commands <release-commands>`.


Add additional environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your application may require additional environment variables in production. :ref:`Apply any enviroment variables
<environment-variables-settings>` using the Divio Control Panel or CLI.


Push local database/media content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have local database or media content, push them to the Test environment:

..  code-block:: bash

    divio project push db
    divio project push media


Deploy the Test server
~~~~~~~~~~~~~~~~~~~~~~

Deploy with:

..  code-block:: bash

    divio project deploy

(or use the **Deploy** button in the Control Panel).

Once deployed, your project will be accessible via the Test server URL shown in the Control Panel.
