.. raw:: html

    <style>
        div[class^=highlight] .manual pre {color: gray;}
        .highlight .segment {font-weight: bold;}
        .highlight .command {color: brown}
        .highlight .action {color: maroon}
        .highlight .namespace {color: navy}
        .highlight .addonname {color: olive}
        .highlight .versionnumber {color: green}
        .highlight .code {font-style: italic}
    </style>


.. _tutorial-flavours-php-add-application:

Add a new package to the project
===================================

There are various ways to add packages to PHP projects, but since this project is managed using `Flavours
<https://www.flavours.dev>`_, we'll use that. Flavours is a platform-independent specification for building
containerised web projects; the Flavours *addon manager* for PHP Laravel - `flavour/fam-php-laravel
<https://hub.docker.com/r/flavour/fam-php-laravel>`_ - knows how to add a package to a Laravel project.

We will add the `laravel-responsecache <https://www.laravelplay.com/packages/spatie::laravel-responsecache>`_ package.
It's an open-source addon, released the Belgian agency `Spatie <https://spatie.be/opensource>`_, and can improve
performance of Laravel sites by caching responses.


Install the Flavours CLI
------------------------

The Flavours CLI is an open-source package, `published at GitHub <https://github.com/flavours/cli>`_.

Run::

    npm install -g @flavour/cli


Run the ``flavour add`` command
-------------------------------

Run the ``flavour add`` command, as follows:

..  code-block:: bash

    ➜ flavour add composer/spatie/laravel-responsecache:6.1.1
      ❯ Installing composer/spatie/laravel-responsecache:6.1.1
        ✔ Getting metadata
        ✔ Checking validity
        ✔ Adding requirement
      ✔ Installed composer/spatie/laravel-responsecache:6.1.1

``laravel-responsecache`` is now installed in the project.


About the command
~~~~~~~~~~~~~~~~~

The command breaks down thus:

.. raw:: html

    <div class="highlight-default notranslate">
    <div class="highlight manual">
    <pre>
      <span class="upperrow"><span class="segment command">flavour</span> <span class="segment action">add    </span> <span class="segment namespace">composer</span>/<span class="segment addonname">laravel-responsecache</span>:<span class="segment versionnumber">6.1.1</span></span>
      <span class="code"><span class="segment command">command</span> <span class="segment action">action</span> <span class="segment namespace">namespace</span>/<span class="segment addonname">addon name</span>           :<span class="segment versionnumber">version number</span></span>
    </pre>
    </div>
    </div>

The Flavours CLI looks up the open Flavours registry at https://addons.flavours.dev, and finds `the particular version
there <https://addons.flavours.dev/addonversions/b0ffad46-3418-4898-b0f7-1b50313906ed/>`_, and pulls down the YAML data
it contains.

The CLI uses the information provided about the addon to identify the appropriate addon manager, which processes
the YAML and performs the steps required by the *add* action.


Check what the command has done to the project
---------------------------------------------------

In this case, the addon manager will apply some changes to the project. You can see what they are by running ``git
diff``:

In its ``app.flavour``, which includes Flavours description of the project, you'll find in the ``addons`` section::

    'composer/spatie/laravel-responsecache:6.1.1':
        manager: 'flavour/fam-php-laravel:0.1.1'
        hash: 9c5f4b2311089d4c5b0def4a0ded5bd927ddd8936d7db18da4cb84283e3413d1

``app.flavour`` is in essence what makes a project Flavours-aware.

And on the project's ``composer.json`` ``require`` section, the addon is listed as a component of the project, so that
when the project is built, the addon will be installed::

    "spatie/laravel-responsecache": "6.1.1"

Finally, if it wasn't there already, you will find a ``.flavour`` directory, which contains information about the addon
and some configuration for it.

Rebuild the project::

    docker-compose build web

When you start the project again with ``docker-compose up`` it will now be running with ``laravel-responsecache``
installed and activated.


Deploy to the Cloud
-------------------

Push your code
~~~~~~~~~~~~~~

To deploy your changes to the Test server, push your changes, and run a deployment command:

..  code-block:: bash

    git add composer.json app.flavour .flavour
    git commit -m "Added laravel-responsecache"
    git push origin master
    divio project deploy test

Divio's hosting service is Flavours-aware; your changes, once pushed and deployed on the Control Panel, will
automatically use the ``composer.json`` file to rebuild the project with the new package installed.


Push the database
~~~~~~~~~~~~~~~~~

Using ``divio project push/pull``
---------------------------------

Your cloud database hasn't yet been migrated, unlike the local database. One very useful function of the Divio CLI is
ability to push and pull your database and media storage to and from the cloud environments. Push the database with:

..  code-block:: bash

    divio project push db

The local database will be pushed to the cloud Test environment; you'll see it the records there after a few moments.

Similarly, you can push/pull media files, and also specify which cloud environment. See the :ref:`local commands
cheatsheet <cheatsheet-project-resource-management>`. A common use-case is to pull live content into the development
environment, so that you can test new development with real data.


Explore configuration
---------------------

As a Flavours-aware host, the Divio Control Panel recognises the newly installed package. In the project's *Addons*
view in the Dashboard, you will see it listed along with its version number and configuration options:

.. image:: /images/flavours-installed-addon.png
   :alt: ''

From its options menu, select *Configure*. You will be presented with a pane of default options (some of which you can
edit). These defaults were contained in the addon's YAML. If you hit **Save**, your options will be applied as
environment variables (you can see them in the *Env Variables* view).

When next deployed, those variables will be applied.


Where to go next?
------------------

This completes the basic cycle of project creation, development and deployment; you should now be familiar with the
fundamental concepts and tools involved.

Other sections of the documentation expand upon them. The :ref:`how-to guides <how-to>` in particular cover many
common operations. And if there's something you're looking for but can't find, please contact Divio support.
