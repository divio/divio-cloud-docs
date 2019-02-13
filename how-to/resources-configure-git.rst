.. _configure-version-control:

How to set up Git hosting for your project
=======================================================

All Divio Cloud projects can use the Git private server we provide. If you prefer, you can instead use a Git hosting
provider of your choice.

..  important::

    Once you have set up an external Git provider on a project, **you will no longer be able to revert to Divio's own
    Git server**. Please ensure that this is what you want to do before using this feature.


Set up external Git hosting
---------------------------

Prepare the external Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need a new repository on the provider ready for your Divio project. Any standard Git hosting provider should
work well, though you may find that some aspects of the configuration that you will need to do will differ a little
between them.

Depending on whether you are *migrating an existing Divio Cloud project's Git hosting* or *creating a new Divio Cloud
project* there are some important steps to take:


Migrating an existing Divio Cloud project's Git hosting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..  danger::

    The migration process *will delete your project's code from the Divio Cloud server* before restoring it from the
    new Git remote.

    You **must** ensure that the new Git remote holds the latest code for the project **before** completing the
    migration process. **Read the steps below carefully.**


* Ensure that in the local version of your repository all the branches you wish to keep are present and up to date
  with the Divio Cloud server: ``git pull <branch>``
* Create the new remote repository.
* Add the new Git repository to the local version of your project as a new Git remote: ``git remote add external
  <repository URL>``.
* Push the branches you require to the new remote: ``git push external <branch>``


Creating a new Divio Cloud project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Create the new remote repository.

The repository **must** have a ``master`` branch, which **must not** contain anything other than ``.git``, ``LICENSE``,
``README``, ``README.md`` or ``README.rst``. If these conditions are not met, the Control Panel will not accept the
repository URL.


.. _git-repository-add-url:

Add the Git repository URL to the Control Panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* For a new Divio Cloud project: select *Repository* > *Custom* in the project creation page.
* For an existing project that you are migrating: select *Repository* from your project's menu in the Dashboard, then
  **Migrate to external repository**.

When asked, enter the repository URL that you would use if cloning the project, for example
``git@github.com/user/repository.git``.


SSH or HTTPS URLs?
^^^^^^^^^^^^^^^^^^

By default, the Control Panel will assume that you will be using SSH, even if you don't actually specify it.

SSH is preferred. HTTPS can be useful in environments where SSH is not permitted, and is available however if you
explicitly provide an HTTPS URL. HTTPS is not available for services whose authentication methods could require you to
share your password with us.

Continue to:

* :ref:`SSH set-up steps <git-setup-ssh>`
* :ref:`HTTPS set-up steps <git-setup-HTTPS>`


.. _git-setup-ssh:

SSH: Add your project's public key to the Git project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next step is give your Divio Project access to the Git repository. This is done by lodging the Divio Project's
*public key* with the repository.

A public key will be generated for you to copy. Add it to the settings of the Git repository.

..  admonition:: Regenerating the public key

    You can regenerate the key at any time, invalidating the old one. This also happens automatically if you change the
    repository URL in our Control Panel.

At this point the Control Panel will test its access by performing a ``git pull`` action. If all is successful, the project Dashboard will now show the repository URL, and inform you that the webhook has not yet been set up.

Go on to :ref:`git-setup-webhook`


.. _git-setup-HTTPS:

HTTPS: Add the Git project's username and password to the Control Panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can give the Divio Project access to the Git repository over HTTPS by providing the Git hosting username and
and a personal access token.

This is *disabled* for those providers that would allow us to connect using your *password*. In accordance with our
security policies, Divio Cloud will not request or store your passwords for other services.

Some Git providers enforce the use of personal access tokens for HTTPs, rather than allowing passwords to be used.
However, GitHub, GitLab and BitBucket all permit HTTPS authentication without the protection of two-factor
authorisation, and for this reason we do not permit HTTPS as an authentication method for these platforms.


.. _git-setup-webhook:

Configure a webhook for the Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A webhook is needed to allow the Git repository to send signals to the Control Panel, so that the Control Panel can
be aware of new events. In the *Repository* view, select the appropriate webhook type (GitHub, GitLab and BitBucket
each have their own type of webhook. Other providers will generally use a webhook that is similar to one of these).

At the Git host, add a new webhook.

The Control Panel will give you a URL to use for the webhook. GitHub for example refers to this as its *Payload URL*. The Control Panel will also give you a secret key.

The only event type that the webhook should respond to are *push* events.

Once the webhook is active and saved, new push events on the repository will send a request to the Control Panel with
the specified URL and the secret key. The Control Panel will immediately pull the change into its own local project,
making them available for you to deploy.


.. _read-only-repository:

Read-only access to the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In most cases, you will want to allow write access to the repository. This is the standard configuration and gives you
full access to the benefits of the Divio Cloud addon system, in which the Control Panel records interface actions and
addon configuration as Git commits.

It's also possible to maintain stricter control over the repository, allowing only read access. In this case, project
configuration that would normally be maintained via the Control Panel must be undertaken manually.

*Write access is required to set up the external Git configuration*, but may be disabled subsequently. If you need to
set up a read-only configuration in which the Control Panel is never able to write to the repository, please contact
Divio support and we handle this for you manually.


Errors and what they mean
~~~~~~~~~~~~~~~~~~~~~~~~~

The remote repository requires a ``master`` branch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Control Panel expected to find a branch (by default named ``master``) at the remote.

If the Divio Cloud project uses the *Custom tracking branches* feature, then whatever branch is used for the *Test*
environment should be present at the remote.

Check the repository for the expected branch.


Authentication error
^^^^^^^^^^^^^^^^^^^^

The most likely problem is that one or more of:

* the :ref:`URL of the Git repository <git-repository-add-url>` entered into the Control Panel
* (for SSH) the :ref:`Control Panel public key <git-setup-ssh>` that you added to the deploy keys of the Git repository, and the deploy keys must have corewct read/write access
* (for HTTPS) the :ref:`Git repository username/personal access token <git-setup-https>` that you added to the Control
  Panel

are not correct. Check these values.


The ``master`` branch must exist and only include a single readme file in order to create a new project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``master`` branch at the remote repository contained other files.

Check that no other files are in the branch.


You have no webhook set up
^^^^^^^^^^^^^^^^^^^^^^^^^^

Although the Control Panel has been able to connect to the repository and authenticate, a webhook has not yet been set
up.

This is not necessarily an error, but it does mean that your Divio Cloud project will not automatically receive signals
from the remote when new commits are made to it, and so you will need to use the manual **Update** button to pull new
changes to your project.

Using webhooks is recommended.
