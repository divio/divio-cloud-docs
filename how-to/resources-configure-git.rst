.. raw:: html

    <style>
        .row {clear: both}

        .column img {border: 1px solid black;}

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


.. _configure-version-control:

How to set up Git hosting for your project
=======================================================

All Divio Cloud projects can use the Git private server we provide. This article describes how you can instead use the
Git hosting provider of your choice.

..  important::

    Once you have set up an external Git provider on a project, **you will no longer be able to revert to Divio's own
    Git server**. Please ensure that this is what you want to do before using this feature.


Set up external Git hosting
---------------------------

Prepare the external Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new repository at the Git provider.

What you do next depends on whether you are creating a new Divio Cloud project, or migrating an existing project:

.. rst-class:: clearfix row

.. rst-class:: column column2

Creating a new Divio Cloud project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure the new repository has a ``master`` branch.

It shouldn't contain anything other than ``.git``, ``LICENSE``, ``README``, ``README.md`` or ``README.rst``.

If these conditions are not met, the Control Panel will not accept the repository URL.


.. rst-class:: column column2

Migrating an existing project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Add the new Git repository to the local version of your project as a new Git remote: ``git remote add external
  <repository URL>``.
* Ensure that all the branches you wish to keep are present and up to date with the Divio Cloud server: ``git pull
  <branch>``
* Push the branches you require to the new remote: ``git push external <branch>``


.. rst-class:: clearfix row

.. _git-repository-add-url:

Add the Git repository URL to the Control Panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need to supply the URL (we recommend using SSH URLs - but :ref:`you can also use HTTPS URLs <git-setup-HTTPS>`
if you prefer) of your new repository to the Control Panel. The next step depends whether this is a new or
existing Divio project:


.. rst-class:: clearfix row

.. rst-class:: column column2

Creating a new Divio Cloud project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Select *Repository* > *Custom* in the project creation page.


.. rst-class:: column column2

Migrating an existing project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Select *Repository* from your project's menu in the Dashboard.
* **Migrate to external repository**.


.. rst-class:: clearfix row

.. _git-setup-ssh:

Add your project's public key to the Git host
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Divio Control Panel will provide you with a public key to add to the Git host, allowing our infrastructure to
access the repository (:ref:`see below for HTTPS <git-setup-HTTPS>`).

Copy the key, and add it to the Git repository:


.. rst-class:: clearfix row

.. rst-class:: column column3

GitHub
^^^^^^

In the repository, go to *Settings* > *Deploy keys* > *Add deploy key*. Select *Allow write access*.


.. rst-class:: column column3

GitLab
^^^^^^

In the repository, go to *Settings* > *Repository* > *Deploy keys* > *Create a new deploy key*. Select *Write access
allowed*.


.. rst-class:: column column3

BitBucket
^^^^^^^^^

Go to *Bitbucket settings* > *SSH keys* > *Add key*. The key will allow push access to all your Bitbucket projects; if
you don't want this, create a Bitbucket account specifically for your Divio Cloud projects.


.. rst-class:: clearfix row

Testing access
~~~~~~~~~~~~~~

When you hit **Continue** in the Control Panel, it tests its access by performing a ``git pull`` action. If all is
successful, the project Dashboard will now show the repository URL, and inform you that the webhook has not yet been
set up.

Go on to :ref:`git-setup-webhook`




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


SSH or HTTPS URLs?
^^^^^^^^^^^^^^^^^^

By default, the Control Panel will assume that you will be using SSH, even if you don't actually specify it.

SSH is preferred. HTTPS can be useful in environments where SSH is not permitted, and is available however if you
explicitly provide an HTTPS URL. HTTPS is not available for services whose authentication methods could require you to
share your password with us.

Continue to:

* :ref:`SSH set-up steps <git-setup-ssh>`
* :ref:`HTTPS set-up steps <git-setup-HTTPS>`

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
