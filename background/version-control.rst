.. _version-control:

Version control
==============================

..  seealso::

    * :ref:`How to configure a Git remote for your project
      <configure-version-control>`


Divio Cloud projects use Git for version control.

By default, projects use our own Git server.

We also offer the option to manage your project's codebase on remote Git providers. Currently, we
support GitHub, GitLab and BitBucket (other options may also work or can be available on request,
including private Git servers, for suitable projects).

Our Control Panel interacts with different Git providers via an abstraction layer that makes it
possible to present common user and application interfaces.


Project repository branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, each project's code is in its Git ``master`` branch, and can be deployed directly from
the Git server to the *Test* or *Live* servers (our strongly-recommended workflow is always to
deploy to *Test* first).


Custom Tracking Branches
^^^^^^^^^^^^^^^^^^^^^^^^

However, on request the *Custom Tracking Branches* feature can be enabled for a project, allowing
different branches to be set for the *Test* and *Live* servers - for example, ``develop`` and
``master`` respectively.

In this workflow you would work on ``develop`` before manually merging into ``master``, and then
deploying *Live*.

All commits made by our Control Panel are to the branch used by the *Test* environment. For example, the *Addons* view
in the Control Panel displays (and only affects) the configuration of the Test environment. When you use *Custom
Tracking Branches*, the Live environment configuration is untouched except by Git operations that explicitly target its
branch.
