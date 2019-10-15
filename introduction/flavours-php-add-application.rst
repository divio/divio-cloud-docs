.. raw:: html

    <style>
        div[class^=highlight] .manual pre {color: gray;}
        .highlight .segment {font-weight: bold;}
        .highlight .cli {color: brown}
        .highlight .command {color: maroon}
        .highlight .namespace {color: navy}
        .highlight .addonname {color: olive}
        .highlight .versionnumber {color: green}
        .highlight .code {font-style: italic}
    </style>


.. _tutorial-flavours-php-add-application:

Add a new package to the project
===================================

There are various ways to add packages to PHP projects, but since this project is managed using Flavours, we'll use
that. Flavours is a platform-independent specification for building containerised web projects.

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

Run ``flavour add``:

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
    <pre><span class="upperrow"><span class="segment cli">flavour</span> <span class="segment command">add    </span> <span class="segment namespace">composer</span>/<span class="segment addonname">laravel-responsecache</span>:<span class="segment versionnumber">6.1.1</span>
    <span class="code"><span class="segment cli">CLI</span>   <span class="segment command">command</span>   <span class="segment namespace">namespace</span>    <span class="segment addonname">addon name</span>    <span class="segment versionnumber">version number</span>
    </div>
    </div>

The command looks up the open registry at https://addons.flavours.dev, and finds `the particular
version there <https://addons.flavours.dev/addonversions/b0ffad46-3418-4898-b0f7-1b50313906ed/>`_.


Check what the command has done to the project
---------------------------------------------------

The ``flavour`` CLI uses the information it retrieves to apply changes to the project. You can see what they are by
running ``git diff``:

In its ``app.flavour``, which includes Flavours instructions for building the project, in the ``addons`` section::

    'composer/spatie/laravel-responsecache:6.1.1':
        manager: 'flavour/fam-php-laravel:0.1.1'
        hash: 9c5f4b2311089d4c5b0def4a0ded5bd927ddd8936d7db18da4cb84283e3413d1

When the project is built, Flavours will know what version of this addon is to be installed, and where to find it.
``app.flavour`` is in essence what makes a project Flavours-aware.œ

And on the project's ``composer.json`` ``require`` section, the addon is listed as a component of the project, so that
it will be invoked at run-time::

    "spatie/laravel-responsecache": "6.1.1"

When you start up the project again with ``docker-compose up`` it will now be running with ``laravel-responsecache``
installed and activated.


Deploy to the Cloud
-------------------

To deploy your changes to the Test server, push your changes, and run a deployment commmand:

..  code-block:: bash

    git add composer.json app.flavour
    git commit -m "Added laravel-responsecache"
    git push origin master
    divio project deploy test
