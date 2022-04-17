.. _divio-app:

How to install and use the Divio app
====================================

The Divio app helps you run your Divio projects locally in our Docker environment, upload and download media, database
and configuration changes as well as set up a shell environment ready for interaction with the project running in the
Docker container.


Set up the Divio app
--------------------


Installation
~~~~~~~~~~~~

* **Download** the `Divio app here <https://divio.com/developers/#app>`_, which is available for Macintosh, Linux and
  Windows.

* Open the downloaded package and follow the on-screen instructions to install the application.

..  admonition:: Important note for Windows users

    To be able to use the Divio app correctly with Docker Desktop on Windows using WSL2, it's important to follow WSL
    installation instructions and install a linux distribution as described in
    https://docs.microsoft.com/en-us/windows/wsl/setup/environment#install-wsl. 


Logging in
~~~~~~~~~

Once the application is installed and running you can login using your email address and password, or if you signed up
with Google or GitHub, simply copy `the access token <https://control.divio.com/account/desktop-app/access-token/>`_
from the Divio control panel and paste it into the provided field.

Select a workspace folder on your computer where you’d keep all the Divio cloud project files.


Use the Divio app
-----------------

Select a project to work with from the list. By default, the list shows all projects, but you can narrow down the
selection by choosing a particular organisation from the dropdown menu.


Set up your local project
~~~~~~~~~~~~~~~~~~~~~~~~~

* Select a project from the list.
* Hit *set up project* to get started.

The Divio app will run through a number of processes to set up the local project. It all happens automatically and takes
just a few minutes.


Launch the site locally
~~~~~~~~~~~~~~~~~~~~~~~

Once the set up process has completed, you can start the local site by launching the local server. 

* Hit **Start** to launch the project.
* If the project has been set up correctly, you can now open the local site in your browser by clicking on the *eye icon*.


Edit project files
~~~~~~~~~~~~~~~~~~
Hit the *folder icon* to open the project folder, use your favorite editor to edit the project files.


Upload/download changes
~~~~~~~~~~~~~~~~~~~~~~~

Use the *Download code* / *Upload code* buttons to push / pull your changes to / from the cloud.

You can also download / upload media files or database changes using the dropdown icon.

.. note::
  
  The Upload/download functionality is better handled with git from your local terminal to be able to pick what to
  commit and to which branch.

Update/rebuild/reset
~~~~~~~~~~~~~~~~~~~~

Open the three vertical dots menu to update, rebuild or reset the project.

*  **Update**: pull down any changes from the Test Server including media and database

*  **Rebuild**: rebuilds the project from the local files

*  **Reset**: tear down the project and start again


Interact with the project
~~~~~~~~~~~~~~~~~~~~~~~~~

Open the project's bash shell by clicking the shell icon ``>_``, to interact with your project directly in its
container.

Launch the Divio Shell
~~~~~~~~~~~~~~~~~~~~~~

As well as a bash shell specific to each project, the Divio app can set up a general shell that is configured to
interact with the cloud. 

To use the Divio shell, hit *OPEN SHELL* in the Divio app and in a few moments you'll be in a terminal shell session.

The Divio shell runs in a Docker container of its own. In this Divio shell, you can also run Divio cli commands, such as

..  code-block:: bash

    divio app list

You cannot interact directly with project containers in the Divio shell. Instead, you should cd into the project
directory locally, and precede your commands with docker-compose run web , for example:

..  code-block:: bash

    docker-compose run web python manage.py

Distinction between the Divio shell and the local container bash shell:

*  the Divio shell is for managing local projects and interacting with the Divio cloud
*  the local container bash shell is for operations inside local projects 


..  Further resources
    ----------------- 

    :ref:`Divio app reference <divio-app-ref>`  
