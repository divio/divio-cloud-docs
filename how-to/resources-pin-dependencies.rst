.. _manage-dependencies:

How to pin all of your project's Python dependencies
====================================================

The Divio Cloud addons and other Python packages in your project have Python *dependencies*:
packages that they install. Dependencies can in turn themselves have dependencies. If a dependency
is *unpinned* (that is, a particular version is not specified in the project's requirements) pip
will generally install the latest version of it, even if a different version was previously
installed.

For example, if your ``requirements.in`` (or the requirements of any other package in the project)
contains::

    rsa==1.3.4
    django-storages

then while you are guaranteed that version 1.3.4 of the ``rsa`` package will be installed the next
time the project is built, you can't be sure in the case of ``django-storages``.

This means that when ``django-storages`` is updated and released to PyPI, an unexpected change can
creep in to your project. You don't need to change anything in your project: *simply redeploying
the project will be enough for the new version to be installed*.

The change might cause a deployment error, or even worse, a run-time error, and you will need to
identify and pin the changed package in order to proceed.

To prevent this from occurring, you can pin *all* the dependencies in your project.

Compile ``requirements.txt``
----------------------------

First, you need to have a working local set-up.

Now you can run::

    docker-compose run --rm web pip-reqs compile

You won't see any output, but you will now find a ``requirements.txt`` file in the project,
containing a list of *all* the packages in the environment, along with their versions.

When your project is built using the new ``requirements.txt`` instead of ``requirements.in``,
you'll have a guarantee that no unexpected changes will be permitted to find their way in to the
project.


Amend the ``Dockerfile``
~~~~~~~~~~~~~~~~~~~~~~~~

In order to have your project built using ``requirements.txt`` instead of ``requirements.in``, you
need to remove the ``pip-reqs compile`` instruction from your project's ``Dockerfile``.

You can do this in two different ways:

* **Locally**: edit the ``Dockerfile`` to remove the ``pip-reqs compile`` instruction.

* **Let the Control Panel do it**: push your ``requirements.txt`` file to the project's repository.
  At the next deployment, the Control Panel will recognise the file and amend the ``Dockerfile``
  itself.

If you later remove the ``requirements.txt`` file, the Control Panel will recognise this and will
restore the ``pip-reqs compile`` instruction to the ``Dockerfile`` when the project is next
deployed. Alternatively you can restore it locally yourself.

See :ref:`the Dockerfile reference <dockerfile-reference-python>` for more information about how
the Control Panel populates the ``Dockerfile``.


Re-compile when required
------------------------

Any time a change is made to ``requirements.in``, or to any addons in the project, you will need to
re-compile ``requirements.txt``. If the change is made to an addon via the Divio Control Panel, you
will need to:

* pull the latest changes to your local repository
* run ``docker-compose run --rm web pip-reqs compile`` to compile the pinned requirements
* rebuld it locally to check that it works as expected
* push the updated ``requirements.txt`` back to the cloud.

