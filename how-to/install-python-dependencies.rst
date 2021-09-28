.. _install-python-dependencies:

How to install Python dependencies in a project
===============================================

..  seealso::

    * :ref:`How to install system packages <install-system-packages>`

It's beyond the scope of this documentation to discuss all the ways in which Python dependencies can be installed in
Divio projects. However, the options described here are sufficient to cover most needs.

If you are using Aldryn Django, refer to the section :ref:`python-packages-aldryn` below.


``pip install`` and ``requirements.txt``
----------------------------------------

The simplest option is to list Python requirements in a ``requirements.txt`` file, and include the command:

..  code-block:: Dockerfile

    RUN pip install -r requirements.txt

in the ``Dockerfile``. See :ref:`deploy-django` for an example.

However this is only adequate as a quick expedient in the early stages of development and is **not recommended** beyond
that, as it does not allow for complete pinning of all dependencies.


.. _pinning-dependencies-good-practice:
.. _manage-dependencies:

Pin all dependencies
--------------------

..  warning::

    Unpinned dependencies are the **number one cause of deployment failures**. Nothing in the
    codebase may have changed, but a fresh build can unexpectedly pick up a newly-released
    version of a package.

All Python dependencies, including implicit sub-dependencies, should be pinned to particular versions.

If any dependency is *unpinned* (that is, a particular version is not specified in the project's requirements) ``pip``
will install the latest version it finds, even if a different version was previously installed. This can cause your
your project to fail with an deployment error or worse, a runtime error, the next time it is built - *even if you
didn't change anything in it yourself*.

To pin all dependencies, your project's requirements should be compiled to a complete list of explicitly specified
package versions. This list should then be committed in the project repository, and not be changed until you need to
update dependencies.


With ``pip``
~~~~~~~~~~~~

Once you are able to build and run your application successfully, you know have a working set of Python dependencies
installed. Use ``pip freeze`` to write them in a new file:

..  code-block:: bash

    docker-compose run web pip freeze > compiled_requirements.txt

And then ensure that the pip command in the Dockerfile uses that list:

..  code-block:: Dockerfile

    RUN pip install -r compiled_requirements.txt


Other tools
~~~~~~~~~~~

There are multiple Python tools such as `pip-tools <https://github.com/jazzband/pip-tools/>`_ and `Poetry
<https://python-poetry.org/docs/>`_ that are more sophisticated than ``pip``, that can also generate a complete list of
pinned dependencies.

You can use the tool of your choice. In each case, the tool itself needs to be available in the Docker build
environment. You can expect to find ``pip`` to be installed by default, but other tools will generally need to be
installed manually in the ``Dockerfile``.

An example using ``pip-tools``:

..  code-block:: Dockerfile

    RUN pip install pip-tools==5.5.0
    RUN pip-compile requirements.in
    RUN pip-sync requirements.txt

This installs ``pip-tools``, compiles ``requirements.in`` to ``requirements.txt``, then installs the components listed
in ``requirements.txt``.

Once you have a working set of dependencies, remove the ``pip-compile`` instruction so that the dependencies are pinned
and frozen in ``requirements.txt``.

.. _python-packages-aldryn:

Python package installation in Aldryn Django projects
--------------------------------------------------------

By default, projects using an Aldryn Django ``Dockerfile`` use our own `pip-reqs tool
<https://pypi.org/project/pip-reqs/>`_ to compile a list wheel URLs from :ref:`our wheels proxy server <wheels-proxy>`,
and installs all packages as wheels.

To install Python dependencies an Aldryn project, list them in the ``requirements.in`` file. They need to be *outside*
the:

..  code-block:: Dockerfile

    # <INSTALLED_ADDONS>
    ...
    # </INSTALLED_ADDONS>

tags, since that part of the file is maintained automatically and is overwritten automatically with
the requirements from the Addons system.

This list is processed by the ``pip`` commands in the ``Dockerfile`` when the image is built.


Pinning dependencies in an Aldryn project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compile ``requirements.txt``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, you need to have a working local set-up. Then run:

..  code-block:: Dockerfile

    docker-compose run --rm web pip-reqs compile

This will create a ``requirements.txt`` file in the project, containing a list of *all* the packages in the
environment, along with their versions.

When your project is built using the new ``requirements.txt`` instead of ``requirements.in``,
you'll have a guarantee that no unexpected changes will be permitted to find their way in to the
project.


Amend the ``Dockerfile``
^^^^^^^^^^^^^^^^^^^^^^^^

In order to have your project built using ``requirements.txt`` instead of ``requirements.in``, you
need to remove the ``pip-reqs compile`` instruction from your project's ``Dockerfile``.

First, remove the Divio-specific comment tags from the ``Dockerfile``:

..  code-block:: Dockerfile

    # <PYTHON>
    ...
    # </PYTHON>

otherwise the Control Panel will simply overwrite your changes.

Then remove the ``pip-reqs compile`` instruction, so that ``requirements.txt`` will not be amended at the next build.

The next time you need to create a fresh ``requirements.txt``, run:

..  code-block:: Dockerfile

    docker-compose run web pip-reqs compile


.. _pip-install-from-online-package:

Specifying packages via a URL
-----------------------------

Please use a commit hash when specifying packages via a URL of a tarballed or zipped archive.

For example::

    https://github.com/account/repository/archive/2d8197e2ec4d01d714dc68810997aeef65e81bc1.zip#egg=package-name==1.0


..  important::

    Branch names or tags are not supported as part of the archive name and will break. Please use the commit hash as
    described above.

    Recent versions of ``pip-tools`` require the use of URLS that provide both the ``egg`` fragment and the version
    fragment (for example, ``egg=package-name==1.0``), and will raise a ``Bad Request for url`` error if they encounter
    URLs lacking it. Older versions would allow you to omit the fragment. 

    See also :ref:`bad-request-for-url`.

    ``pip-tools`` does note support `VCS protocols <https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support>`_
    - for example, you cannot use URLs starting with ``git+`` or ``hg+``, such as
    ``git+git@github.com:divio/django-cms.git``. 


.. _vcs-protocol-support:
