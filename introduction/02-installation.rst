.. _tutorial-installation:

Set up the local development environment
========================================

In order to work on your project, we need to set it up in the local development environment. This also uses Docker.

Docker makes it possible to run and work on a project in the same environment as on the cloud, thus side-stepping some
of the most troublesome problems faced by development teams, in which something works well in development, but runs
into problems as a result of different environment conditions in production, or when a another team member tries to set
it up on their own machine.

Using Docker means that not only does every member of the development team work in the same environment - versions of
installed packages, environment variables, database and other services - but they're all in the same evironment that
the application will have in production.


..  admonition:: Older versions of Macintosh OS X and Windows

    Older versions of Macintosh OS X and Windows do not support the native Docker application.
    Instead, they require Docker to be run in a virtual machine (in VirtualBox) while the Docker
    Toolbox application provides a set of tools to interact with it.

    This is considerably more difficult to set up than Docker running natively. It's possible to
    manage, but we are not able to provide support for this combination.

You will need to have the following installed or configured, and know at least the basics of using them, before
proceeding:

* Git (`GitHub's set up Git guide <https://help.github.com/en/github/getting-started-with-github/set-up-git>`_)
* SSH, so that you can provide your public key to a server (`GitHub's guides to setting up SSH
  <https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>`_)
* Pip, the `Python Package Installer <https://pip.pypa.io/en/stable/installing/>`_


Install the Divio CLI package
---------------------------------

The :ref:`Divio CLI application <divio-cli-ref>` is installable using Pip::

    pip install divio-cli

If you already have them installed, check that they are up-to-date::

    pip install --upgrade divio-cli

You can do this in a virtual environment if you prefer not to install it globally. Otherwise, it's a lightweight
component and can easily be removed later if you decide you don't require it.


Log in
------

The Divio CLI needs to be authenticated with the Control Panel in order to
interact with it::

    divio login

This will open your browser at
https://control.divio.com/account/desktop-app/access-token/, where you can copy
an access token to paste into the prompt.


.. _add-public-key:

Add your public SSH key to the Control Panel
--------------------------------------------

The Control Panel needs your public key, so that you can interact with our Git server and so on. Visit `SSH Keys in the
Control Panel <https://control.divio.com/account/ssh-keys/>`_. Add your **public** key. If you're not sure how to
manage SSH keys, see the excellent GitHub articles on `how to connect with SSH
<https://help.github.com/articles/connecting-to-github-with-ssh/>`_.


Install Docker and Docker Compose
----------------------------------

* Macintosh users: `Docker for Mac <https://docs.docker.com/docker-for-mac/>`_
* Windows users: `Docker for Windows <https://docs.docker.com/docker-for-windows/>`_
* Linux users: `Docker CE <https://docs.docker.com/install/#server>`_ and `Docker Compose
  <https://docs.docker.com/compose/install/>`_

(Windows users should consult the :ref:`checklist
<checklist-docker-installation-windows>` below).

Launch Docker. You can check that it's running correctly with::

    docker run --rm busybox true


.. _checklist-docker-installation-windows:

Additional checklist for Docker installation on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* In Docker's settings, make sure that it is set to use *Linux containers*.
* Ensure that your Windows user is in the ``docker-users`` group.
* When you launch Docker, make sure that you do so as a Windows administrator.


You're now ready to set up the project you created in the previously step in your local environment for development
work.
