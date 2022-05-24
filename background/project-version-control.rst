.. _version-control:

Version control
==============================

..  seealso::

    * :ref:`How to configure a Git remote for your application
      <configure-version-control>`
    * :ref:`use-git-manage-project`


Divio applications use Git for version control.

By default, applications use our own Git server.

We also offer the option to manage your application's codebase on remote Git providers. Currently, we
support GitHub, GitLab and BitBucket (other options may also work or can be available on request,
including private Git servers, for suitable applications).

Our Control Panel interacts with different Git providers via an abstraction layer that makes it
possible to present common user and application interfaces.


All commits target the *Test* environment
--------------------------------------------

All commits made by our Control Panel are to the branch used by the *Test* environment. For example, the *Addons* view
in the Control Panel displays (and only affects) the configuration of the Test environment. When you use
:ref:`custom-tracking-branches` (below), the Live environment configuration is untouched except by Git operations that
explicitly target its branch.


Application repository branches
---------------------------------

By default, each project's code is in its Git ``main`` branch, and can be deployed directly from
the Git server to the *Test* or *Live* servers (our strongly-recommended workflow is always to
deploy to *Test* first).


.. _custom-tracking-branches:

Custom Tracking Branches
---------------------------------

Each environment can be configured to track a different Git branch, by editing the *Branch* field in the *Environments*
view. If the branch specified cannot be found, an *Unable to get commit count from repository* message will be shown.

Using custom branches allows (for example) a workflow in which you work on ``develop`` before manually merging into
``main``, and then deploying *Live*.
