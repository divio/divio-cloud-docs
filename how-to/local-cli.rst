..  Do not change this document name!

    Referred to by: tutorial message 103 account-access-token
    Where: https://control.divio.com/account/desktop-app/access-token/

    Referred to by: Readme of Divio CLI
    Where: https://github.com/divio/divio-cli/blob/master/README.md

    Referred to by: PyPI
    Where: https://pypi.org/project/divio-cli/

    As: https://docs.divio.com/en/latest/how-to/local-cli/

.. _local-cli:

How to get started with the Divio CLI
================================================

Although we provide `the Divio app <https://www.divio.com/app/>`_, a GUI
application for working with your projects locally, for many developers the
preferred tool for working with Divio projects is the Divio CLI.

..  seealso::

    If you are completely new to Divio, please see :ref:`our tutorial
    <tutorial-installation>`, which guides you through installation and use of
    the Divio CLI in more detail.


Pre-requisites
--------------

In order to use the Divio CLI, you will need to install various packages if you
do not already have them installed, including:

* Docker
* Git
* Pip


Install the CLI
----------------

The Divio CLI is a Python application. Note that it requires Python 3.6 or higher. Install it with:

..  code-block:: bash

    pip install divio-cli


Log in using the CLI
--------------------

Run::

  divio login

This will open https://control.divio.com/account/desktop-app/access-token/ in
your browser, from where you can copy a token to paste into the terminal.


Add your public key to the Control Panel
----------------------------------------

Upload your public key at https://control.divio.com/account/ssh-keys/.


Usage
-----

The CLI allows you to interact with projects locally and on the Cloud; for
example, to set up a Cloud project locally::

  divio project setup <project slug>

Commonly used commands include those to push and pull database and media, for example::

    divio project pull db

    divio project push media

Where approriate, you can specify a particular environment (default is always Test)::

    divio project push db live

or even another project::

    divio project pull db --remote-id

Similarly, you can do things like view runtime logs::

    divio project logs --tail live

or open the project dashboard::

    divio project dashboard

or associate a local project with a cloud project::

    divio project configure

and to :ref:`manage environment variables <manage-environment-variables>`::

    divio project env-vars

See the :ref:`reference guide <divio-cli-ref>` for full details of commands and options.
