.. _tutorial-installation:

Get started
===========

Create your account
-------------------

A Divio Cloud account is free to set up and use indefinitely. Create your
account on the Divio Cloud `Control Panel <https://control.divio.com/>`_, or
log in there if you already have one.


Install the Divio CLI package
---------------------------------

The :ref:`Divio CLI application <divio-cli-ref>` is installable using pip::

    pip install divio-cli

If you already have it installed, check that it is up-to-date::

    pip install --upgrade divio-cli

You can install this in a virtualenv if you prefer not to install it globally.

..  important::

    You will also need to install the Aldryn Client package (a future update
    will make this unnecessary)::

        pip install aldryn-client


Log in
------

*divio-cli* needs to be authenticated with the Control Panel in order to
interact with it::

    divio login

This will open your browser at
https://control.divio.com/account/desktop-app/access-token/, where you can copy
an access token to paste into the prompt::

    ➜  ~ divio login
    Your browser has been opened to visit: https://control.divio.com/account/desktop-app/access-token/
    Please copy the access token and paste it here: rsYa1d0qDyF6TbI4wzfrdfSKinqSWAoxU7NgN7Cssgg5ndFfk3naghagh7
    Welcome to Divio Cloud. You are now logged in.


Add your public SSH key to the Control Panel
--------------------------------------------

The Control Panel needs your public key, so that you can interact with our Git
server and so on. Visit `SSH Keys in the Control Panel
<https://control.divio.com/account/ssh-keys/>`_. Add your **public** key.

..  note:: Note sure how to manage SSH keys?

    See the excellent GitHub articles on `how to connect with SSH
    <https://help.github.com/articles/connecting-to-github-with-ssh/>`_.


Set up Docker
-------------

At this stage, you have two ways to set up Docker. You can either do it by
hand, or use the :ref:`Divio app <divio-app>` to manage this for you.

We recommend using the Divio app, which is available for Macintosh, Linux and
Windows. (It's especially recommended if you are using a version of Windows
other than Windows 10 Professional.)

If you prefer to do it by hand, see :ref:`docker-ssh-by-hand` below.

`Download the Divio application <https://divio.com/app/>`_ and install it. When
you run it, it will take care of installing and setting up Docker.

The Divio app is also a useful tool when you need technical support - it's
easier for us to assist users who have it installed.


.. _docker-ssh-by-hand:

Set up Docker by hand
---------------------

..  important::

    We recommend that you allow the Divio app to manage installation and configuration.

    Consider a manual installation only if you already know what you are doing!

* Download and install `Docker for Mac <https://www.docker.com/docker-mac>`_ or `Docker for Windows
  <https://www.docker.com/docker-windows>`_.

* Check that it runs correctly and that the Divio app is able to communicate with it.

..  note::

    Older versions of macOS and Windows do not support the native Docker
    application. Instead, they require Docker to be run in a virtual machine
    (in VirtualBox) and the Docker Toolbox application provides a set of tools
    to interact with it.

    This can be more difficult to set up than Docker for Windows, but the Divio
    app will take care of it. **This is the strongly recommended way to set up
    Docker in such a case.**

