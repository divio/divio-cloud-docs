.. _manage-dependencies:

How to pin all of your Aldryn Django project's Python dependencies
==================================================================

..  seealso:: :ref:`infrastructure-python-packaging`

.. _pinning-dependencies-good-practice:

Pinning dependencies is good practice
-------------------------------------

If a dependency is *unpinned* (that is, a particular version is not specified in the project's requirements) pip will
install the latest version it finds, even if a different version was previously installed. This can cause your your
project to fail with an deployment error or worse, a runtime error, the next time it is built - *even if you didn't
change anything in it yourself*.

We strongly recommend that when you add a dependency to a project via its ``requirements.in`` that you pin it to a
particular version, by specifying its version number.

For example, if you use ``rsa`` and know that version ``1.3.4`` works, specify it::

    rsa==1.3.4

That way if a newer, incompatible version of the package is released, your project will still install the correct
version the next time you build or redeploy it.


What about dependencies of dependencies?
-----------------------------------------------

However, dependencies can in turn themselves have dependencies. Even if you pin *your* requirements, their dependencies
may be unpinned.

For example, your project may specify ``some-package==1.2.3``, but if ``some-package`` lists ``rsa`` in its
requirements, then the next time the project is built, it will attempt to do so using the latest version of ``rsa`` -
which might not be compatible.

The solution is to pin *all* the dependencies in your project.

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

..  important::

    If the relevant sections in the ``Dockerfile`` are surrounded by the Divio-specific comment tags::

        # <PYTHON>
        ...
        # </PYTHON>

    remove these tags - otherwise the Control Panel will simply overwrite your changes.

See :ref:`the Dockerfile reference <dockerfile-reference-python>` for more information about how
the Control Panel populates the ``Dockerfile``.


Re-compile when required
------------------------

Any time a change is made to ``requirements.in``, or to any addons in the project, you will need to
re-compile ``requirements.txt``. If the change is made to an addon via the Divio Control Panel, you
will need to:

* pull the latest changes to your local repository
* run ``docker-compose run --rm web pip-reqs compile`` to compile the pinned requirements
* rebuild it locally to check that it works as expected
* push the updated ``requirements.txt`` back to the cloud.

