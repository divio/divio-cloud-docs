.. _tutorial-installation:

Set up the local development environment
========================================

This is the part of the tutorial with the greatest potential for stumbling-blocks, because it involves the installation
of software. However the components are very reliable and the vast majority of users encounter no problems at all.

If you do run into any difficulties, please don't hesitate to contact Divio support, who will be glad to help you out.


Why is the local development environment so important?
-------------------------------------------------------

**Docker** makes it possible to run and work on a project locally in the same environment as it runs on in the cloud.
This side-steps some of the most troublesome problems faced by development teams, in which something works well in
development, but then runs into trouble as a result of different environment conditions in production, or when another
team member tries to set it up on their own machine.

Using Docker means that not only does every member of the development team work *in the same environment* - which
includes versions of installed packages, environment variables, database and other services - but they're all in the
same environment that the application will have in production.

The **local development environment** includes the tools and software that allow you to work on your project, testing
it as you go on your own computer. This uses Docker, just like our cloud deployment architecture. The local environment
is also integrated with the cloud infrastructure - *it's like having a hotline to the cloud*.

In this section we will:

* :ref:`install Docker <install-docker>`
* :ref:`install the Divio CLI <install-divio-cli>`
* :ref:`add your public key to the Divio Control Panel <add-public-key>`


..  admonition:: Older versions of Macintosh OS X and Windows

    Older versions of Macintosh OS X and Windows do not support the native Docker application, but require Docker to be
    run using VirtualBox. This is considerably more complex to set up than Docker running natively. We do not support
    for this combination. Check the system requirements for `Macintosh
    <https://docs.docker.com/docker-for-mac/install/#system-requirements>`_ and `Windows
    <https://docs.docker.com/docker-for-windows/install/#system-requirements>`_.


Before you start
----------------

You will need to have the following installed or configured, and know at least the basics of using them, before
proceeding:

* Git (see `GitHub's set up Git guide <https://help.github.com/en/github/getting-started-with-github/set-up-git>`_)
* SSH, so that you can provide your public key to a server (`GitHub's guides to setting up SSH
  <https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh>`_)
* Pip, the `Python Package Installer <https://pip.pypa.io/en/stable/installing/>`_


.. _install-docker:

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


.. _install-divio-cli:

Install the Divio CLI package
---------------------------------

The :ref:`Divio CLI application <divio-cli-ref>` is installable using Pip. Note that it requires Python 3.6 or higher.
Depending on your system, you may need to use ``pip3`` in the examples below.

..  code-block:: bash

    pip install divio-cli

If you already have it installed, check that they are up-to-date::

    pip install --upgrade divio-cli

You can do this in a virtual environment if you prefer not to install it globally. Otherwise, it's a lightweight
component and can easily be removed later if you decide you don't require it.


Log in
------

Make sure you are logged in to your account on the Divio `Control Panel <https://control.divio.com/>`_. If you don't
already have one, now is the time to create it (a Divio account is free to set up and use indefinitely).

The Divio CLI needs to be authenticated with the Control Panel in order to
interact with it, using the command::

    divio login

This will open your browser at
https://control.divio.com/account/desktop-app/access-token/, where you can copy
an access token to paste into the prompt. The access token is hidden for security reasons.

.. _login-windows-users:

..  admonition:: Note for Windows users

    If your divio login fails with an invalid token, it could be that the pasting is not working properly and you 
    either *right click* **once** and press *enter* or enable the Ctrl+Shift+C/V as Copy/Paste (Check the box in the 
    “Command Prompt”/ “Windows Powershell” Properties window) and use Ctrl + Shift + V to paste your access token.


.. _add-public-key:

Add your public SSH key to the Control Panel
--------------------------------------------

The Control Panel needs your public key, so that you can interact with our Git server and so on. Visit `SSH Keys in the
Control Panel <https://control.divio.com/account/ssh-keys/>`_. Add your **public** key. If you're not sure how to
manage SSH keys, see the excellent GitHub articles on `how to connect with SSH
<https://help.github.com/articles/connecting-to-github-with-ssh/>`_.

Test that your key is set up correctly; you should receive a ``No interactive access`` response:

..  code-block:: bash

    ssh -T git@git.divio.com


On to the next step
-------------------

Now you're ready to go on to the next step. At this point the tutorial branches, and you can continue working with
Python/Django or PHP/Laravel.

* continue with :ref:`Django from scratch <tutorial-django-set-up>`
* continue with :ref:`Django using the Aldryn addons framework <tutorial-aldryn-set-up>`
* continue with :ref:`Wagtail <wagtail-tutorial-set-up>`
* continue with :ref:`PHP/Laravel <tutorial-flavours-php-set-up>`
