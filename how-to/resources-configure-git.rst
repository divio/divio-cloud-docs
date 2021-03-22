..  Do not change this document name!
    Referred to by: tutorial message 115 alert-can-add-repository
    Where: Control Panel Repository view
    As: https://docs.divio.com/en/latest/how-to/resources-configure-git/

..  Referred to by: tutorial message 150 project-repository-info
    Where: Control Panel Repository view
    As: https://docs.divio.com/en/latest/how-to/resources-configure-git/

..  raw:: html

    <style>
        .row {clear: both}

        @media only screen and (min-width: 1000px),
               only screen and (min-width: 500px) and (max-width: 768px){

            .column {
                padding-left: 5px;
                padding-right: 5px;
                float: left;
            }

            .column2  {
                width: 50%;
            }
            .column3  {
                width: 33%;
            }
        }

        .main-visual {
            margin-bottom: 0 !important;
        }
        h2 {border-top: 1px solid #e1e4e5; padding-top: 1em}
    </style>


.. |github| image:: /images/github.png
   :alt: 'GitHub'
   :width: 28

.. |gitlab| image:: /images/gitlab.png
   :alt: 'GitLab'
   :width: 26

.. |bitbucket| image:: /images/bitbucket.png
   :alt: 'BitBucket'
   :width: 27


.. _configure-version-control:

How to configure external Git hosting
=======================================================

All Divio projects can use the Git private server we provide. This article describes how you can instead use the
Git hosting provider of your choice.

..  important::

    Once you have set up an external Git provider on a project, **you will no longer be able to revert to Divio's own
    Git server**. Please ensure that this is what you want to do before using this feature.

The steps in this process are:

#. :ref:`git-prepare-repo`
#. :ref:`git-repository-add-url` (so the Control Panel can find the codebase)
#. :ref:`git-setup-ssh` (so that the Control Panel is permitted to access the repository)
#. :ref:`git-test-access`
#. :ref:`git-setup-webhook` (so that the repository can push events to the Control Panel)


.. _git-prepare-repo:

Prepare the external Git repository
------------------------------------

Go to your Git hosting service. The next step depends on whether you are *creating a new Divio project*, or
*migrating an existing Divio project*:

..  rst-class:: clearfix row

..  rst-class:: column column2

Creating a new Divio project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order for our Control Panel to be able to check out the Git repository, it must be able to check out the ``master``
branch, with no conflicts.

#. Create a new repository at the Git provider.
#. Ensure the new repository has a ``master`` branch. The branch must not contain anything other than ``.git``,
   ``LICENSE``, ``README``, ``README.md`` or ``README.rst``.

If these conditions are not met, the Control Panel will not accept the repository URL.


..  rst-class:: column column2

Migrating an existing Divio project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Add the Git repository to the local version of your project as a remote: ``git remote add external <repository URL>``.
#. Ensure that all the branches you wish to keep are present and up to date with the Divio server: ``git pull <branch>``
#. Push the branches you require to the new remote: ``git push external <branch>``


..  rst-class:: clearfix row

.. _git-repository-add-url:

Add the Git repository URL to the Control Panel
------------------------------------------------------------------------

You will need to supply the URL (SSH URLs are recommended, but :ref:`you can also use HTTPS URLs <git-setup-HTTPS>`) of
your new repository to the Control Panel. The next step depends on whether this is a new or existing Divio project:


..  rst-class:: clearfix row

..  rst-class:: column column2

Creating a new Divio project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Select *Repository* > *Custom* in the project creation page.


..  rst-class:: column column2

Migrating an existing Divio project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Select *Repository* from your project's menu in the Dashboard.
#. Select **Migrate to external repository**.


..  rst-class:: clearfix row

.. _git-setup-ssh:

Add your project's public key to the Git host
------------------------------------------------------------------------

The Divio Control Panel will provide you with a public key to add to the Git host, allowing our infrastructure to
access the repository (:ref:`see below for HTTPS <git-setup-HTTPS>`).

Copy the key, and add it to the Git repository:


|github| GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. In the repository, go to *Settings* > *Deploy keys* > *Add deploy key*.
#. Paste the key.
#. Select *Allow write access*.


|gitlab| GitLab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. In the repository, go to *Settings* > *Repository* > *Deploy keys* > *Create a new deploy key*.
#. Paste the key.
#. Select *Write access allowed*.


|bitbucket| BitBucket
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Optionally, create a Bitbucket account specifically for Divio projects - otherwise the key will grant
   access to all your Bitbucket projects.
#. Go to *Bitbucket settings* > *SSH keys* > *Add key*.
#. Paste the key.


.. _git-test-access:

Test access
------------------------------------------------------------------------

When you hit **Continue** in the Control Panel, it tests its access by performing a ``git pull`` action. If
successful, the project Dashboard will show the repository URL.


.. _git-setup-webhook:

Configure a webhook for the Git repository (optional)
------------------------------------------------------------------------

In order for the Control Panel to receive a signal when the repository is updated, you need to set up a webhook. This
step is optional but strongly recommended for convenience.

In the *Repository* view, select the appropriate webhook type (GitHub, GitLab and BitBucket each have their own type of
webhook. Other providers will generally use a webhook that is similar to one of these).

The Control Panel will give you a URL to use for the webhook, and a secret key.

At the Git host, add a new webhook:


|github| GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. In the repository, go to *Settings* > *Webhooks* > *Add webhook*.
#. Add the Webhook URL to the *Payload URL* field.
#. Leave the *Content type* as ``application-x/www-form-urlencode``.
#. Add the Webhook Shared Secret to the *Secret* field.
#. Set *Push events* as the trigger for the webhook.


|gitlab| GitLab
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. In the repository, go to *Settings* > *Integrations*.
#. Add the Webhook URL to the *URL* field.
#. Add the Webhook Shared Secret to the *Secret token* field.
#. Leave the *Push events* trigger set.


|bitbucket| BitBucket
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. In the repository, go to *Settings* > *Webhooks*.
#. Give the webhook a *title*.
#. Add the Webhook URL to the *URL* field.
#. For *Triggers*, ensure that *Repository push* is set.

The Webhook Shared Secret is not used.


Using the external Git remote
------------------------------------------------------------------------

Your external Git remote has now been set up.

The Control Panel can save commits to it (using :ref:`the key you provided <git-setup-ssh>`) and the repository can
send a signal to the Control Panel to pull in new commits when they land (using :ref:`the webhook <git-setup-webhook>`).


Remote Git: Reset to origin
----------------------------

For projects with external git repositories, especially if commits are force pushed, the project's repository on the
control panel may not reflect all the commits made in its remote repository at ``origin``. 

To reset to remote, go to the *repository* view of the project's control panel and select *reset to origin*
and the repository will reflect the commit history of the remote ``origin``.


Options and special cases
-------------------------

.. _read-only-repository:

Read-only access to the repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In most cases, you will want to allow write access to the repository. This is the standard configuration and gives you
full access to the benefits of the Divio addon system, in which the Control Panel records interface actions and
addon configuration as Git commits.

It's also possible to maintain stricter control over the repository, allowing only read access. In this case, project
configuration that would normally be maintained via the Control Panel must be undertaken manually.

*Write access is required to set up the external Git configuration*, but may be disabled subsequently.


.. _git-setup-HTTPS:

HTTPS authentication
~~~~~~~~~~~~~~~~~~~~

By default, the Control Panel will assume that you will be using SSH authentication to the Git provider, which is
preferred.

However, HTTPS can be useful in environments where SSH is not permitted, and is available if you explicitly provide an
HTTPS URL.

You can give the Divio Project access to the Git repository over HTTPS by providing the Git hosting username and a
personal access token.

This is *disabled* for those providers that would allow us to connect using your *password*. In accordance with our
security policies, Divio will not request or store your passwords for other services.

Some Git providers enforce the use of personal access tokens for HTTPs, rather than allowing passwords to be used.
However, GitHub, GitLab and BitBucket all permit HTTPS authentication using account passwords, and for this reason we
do not permit HTTPS as an authentication method for these platforms.


Errors and what they mean
-------------------------

The remote repository requires a ``master`` branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Control Panel expected to find a branch (by default named ``master``) at the remote.

If the Divio project uses the *Custom tracking branches* feature, then whatever branch is used for the *Test*
environment should be present at the remote.

Check the repository for the expected branch.


Authentication error
~~~~~~~~~~~~~~~~~~~~

The most likely problem is that one or more of:

* the :ref:`URL of the Git repository <git-repository-add-url>` entered into the Control Panel
* (for SSH) the :ref:`Control Panel public key <git-setup-ssh>` that you added to the deploy keys of the Git repository, and the deploy keys must have correct read/write access
* (for HTTPS) the :ref:`Git repository username/personal access token <git-setup-https>` that you added to the Control
  Panel

are not correct. Check these values.


The ``master`` branch must exist and only include a single readme file in order to create a new project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``master`` branch at the remote repository contained other files.

Check that no other files are in the branch.


You have no webhook set up
~~~~~~~~~~~~~~~~~~~~~~~~~~

Although the Control Panel has been able to connect to the repository and authenticate, a webhook has not yet been set
up.

This is not necessarily an error, but it does mean that your Divio project will not automatically receive signals
from the remote when new commits are made to it, and so you will need to use the manual **Update** button to pull new
changes to your project.

Using webhooks is recommended.
