.. _tutorial-installation:

Get started
===========

Create your account
-------------------

A Divio Cloud account is free to set up and use indefinitely. Create your
account on the Divio Cloud `Control Panel <https://control.divio.com/>`_, or
log in there if you already have one.

Our Divio GUI application can set up all you need to get started. In this tutorial however we will
install and configure the components - Docker, the Divio CLI, and so on - manually. This will give
more experienced developers a better insight into the system and how it all works together.

We expect you to have Pip and Git installed and to have at least a basic understanding of their
usage.

..  admonition:: Older versions of Macintosh OS X and Windows

    Older versions of Macintosh OS X and Windows do not support the native Docker application.
    Instead, they require Docker to be run in a virtual machine (in VirtualBox) while the Docker
    Toolbox application provides a set of tools to interact with it.

    This can be more difficult to set up than Docker running natively, but the Divio app will take
    care of it. **This is the strongly recommended way to set up Docker in such a case.**

    If you're using one of these older systems and cannot upgrade, please download and run the
    Divio app. With some fairly minor differences, you'll be able to follow this tutorial using the
    Divio Shell that the app provides.

    `Download the Divio application <https://divio.com/app/>`_ and install it. When you run it, it
    will take care of installing and setting up Docker the components you require.

    Continue at :ref:`tutorial-set-up`.


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


.. _add-public-key:

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

Download and install `Docker for Mac <https://www.docker.com/docker-mac>`_ or `Docker for Windows
<https://www.docker.com/docker-windows>`_.

Launch Docker. Check that it's running correctly with::

    docker run --rm busybox true

