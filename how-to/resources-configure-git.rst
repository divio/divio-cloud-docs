.. _configure-version-control:

How to set up Git hosting for your project
=======================================================

All Divio Cloud projects can use the Git private server we provide. If you prefer, you can instead use the Git hosting
provider of your choice.


..  important::

    Once you have set up an external Git provider on a project, **you will no longer be able to revert to Divio's own
    Git server**. Please ensure that this is what you want to do before using this feature.


Set up external Git hosting
---------------------------

.. _git-repository-add-url:

Add the Git repository URL to the Control Panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The external Git repository can be set up either:

* at project creation time: select *Repository* > *Custom* in the project creation page
* later: select *Repository* from your project's menu in the Dashboard, then **Migrate to external repository**

In most cases, you will have created a new repository on the provider ready for this. Enter the repository URL - you
can use different formats, for example:

* git@github.com/user/repository.git
* https://github.com/user/repository
* other
* examples

The repository **must** have a ``master`` branch, which **must** be empty. If not, you will not be able to add the
repository URL in the Divio Control Panel.


SSH or HTTPS?
^^^^^^^^^^^^^

By default, the Control Panel will assume that you will be using SSH, even if you don't actually specify it. However
you can explicitly provide an HTTPS URL, in which case the Control Panel will also request the associated username and
password. Generally, SSH is easier, but HTTPS can be useful in environments where SSH is not permitted.

Continue to:

* :ref:`SSH set-up steps <git-setup-ssh>`
* HTTPS set-up steps


.. _git-setup-ssh:

SSH: Add your project's public key to the Git project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next step is give your Divio Project access to the Git repository. This is done by lodging the Divio Project's
*public key* with the repository.

A public key will be generated for you to copy. Add it to the settings of the Git repository:

* GitHub: *Deploy keys* > **Add deploy key**. Make sure you *Allow write access*, unless this is to be a
  :ref:`read-only repository <read-only-repository>`.
* GitLab:

..  admonition:: Regenerating the public key

    You can regenerate the key at any time, invalidating the old one. This also happens automatically if you change the
    repository URL in our Control Panel.

At this point the Control Panel will test its access by performing a ``git pull`` action. If all is successful, the project Dashboard will now show the repository URL, and inform you that the webhook has not yet been set up.

Go on to :ref:`git-setup-webhook`


.. _git-setup-HTTPS:

HTTPS: Add the Git project's username and password to the Control Panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can give the Divio Project access to the Git repository over HTTPS by providing the Git hosting username and
password.


GitHub
^^^^^^

GitHub requires you to use a *personal access token* in place of your password. `Generate a new token
<https://github.com/settings/tokens/new>`_. The token will need access to the *Repo* functions.

Paste that into the *password* field in the Control Panel dialog.


.. _git-setup-webhook:

Configure a webhook for the Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A webhook is needed to allow the Git repository to send signals to the Control Panel, so that the Control Panel can
be aware of new events. In the *Repository* view, select the appropriate webhook type (GitHub, GitLab and BitBucket
each have their own type of webhook. Other providers will generally use a webhook that is similar to one of these).

In the repository settings at the Git host, add a new webhook.

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

<describe affected files and operations here>


Errors and what they mean
~~~~~~~~~~~~~~~~~~~~~~~~~

Authentication error
^^^^^^^^^^^^^^^^^^^^

The most likely problem is that one or more of:

* the :ref:`URL of the Git repository <git-repository-add-url>` entered into the Control Panel
* (for SSH) the :ref:`Control Panel public key <git-setup-ssh>` that you added to the deploy keys of the Git repository
* (for HTTPS) the :ref:`Git repository username/password <git-setup-https>` that you added to the Control Panel

are not correct.

This can also occur if the repository does not contain an empty ``master`` branch.


Unable to get commit count from repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have no webhook set up
^^^^^^^^^^^^^^^^^^^^^^^^^^