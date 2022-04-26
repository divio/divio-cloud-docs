..  Do not change this document name!

    Referred to by: tutorial message 103 account-access-token
    Where: https://control.divio.com/account/desktop-app/access-token/

    Referred to by: Readme of Divio CLI
    Where: https://github.com/divio/divio-cli/blob/master/README.md

    Referred to by: PyPI
    Where: https://pypi.org/project/divio-cli/

    As: https://docs.divio.com/en/latest/how-to/local-cli/

.. _local-cli:

How to set up the Divio local development environment
===============================================================

This document guides you through the installation and basic configuration of components required to set up
a working local environment for Divio projects, so that you can run them on your own computer, and interact
with the Divio Control Panel and the same projects deployed on our cloud infrastructure.

..  seealso::

    This document assumes you are a reasonably experienced software developer. If you are completely new to Divio and
    the tools mentioned here, please see :ref:`our tutorial <tutorial-installation>`, which guides you through the
    process in more detail.


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

This will open your browser at
https://control.divio.com/account/desktop-app/access-token/, where you can copy
an access token to paste into the prompt.

⚠️ **For Windows users**: Your terminal might not have copying and pasting shortcuts such as Ctrl+C/Ctrl+V enabled by default. Make sure that
you can use those shortcuts before you provide your access token as the input will be hidden for security reasons.

Add your public key to the Control Panel
----------------------------------------

Upload your public key at https://control.divio.com/account/ssh-keys/.


.. _local-cli-usage:

Usage
-----

The CLI allows you to interact with projects locally and on the Cloud; for
example, to set up a Cloud project locally::

  divio app setup <project slug>

Commonly used commands include those to push and pull database and media, for example::

    divio app pull db

    divio app push media

Where appropriate, you can specify a particular environment (default is always Test)::

    divio app push db live

or even another project::

    divio app pull db --remote-id

Similarly, you can do things like view runtime logs::

    divio app logs --tail live

or open the project dashboard::

    divio app dashboard

or associate a local project with a cloud project::

    divio app configure

and to :ref:`manage environment variables <manage-environment-variables>`::

    divio app env-vars

See the :ref:`reference guide <divio-cli-ref>` for full details of commands and options.


Next steps for new users
------------------------

If you have a basic familiarity with Docker and cloud deployment, we recommend you follow the
:ref:`deploy-django` guide for a concise, practical walk-through the process of configuring an application
for local development and deployment to our cloud infrastructure.

If Docker, containerisation and cloud deployment are new to you, we recommend that you work through our :ref:`detailed,
beginner-oriented tutorial <introduction>`, which is designed to introduce all the concepts and tools you require in
order to use our platform successfully.
