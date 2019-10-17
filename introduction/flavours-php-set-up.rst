.. _tutorial-flavours-php-set-up:

Set up a new PHP/Flavours project
===================================

..  admonition:: Our Flavours implementation is in private beta

    Access to Flavours on Divio is currently in a *private beta* phase. Sign up for access via `the Flavours website
    <https://www.flavours.dev>`_.


This part of the tutorial will introduce you to the Divio development/deployment workflow using Flavours and a PHP
project as an example.

In this page we will create and deploy a new project in the Control Panel, then replicate it locally.

If you have not already done so, you will need to :ref:`create your Divio account and set up the local development
environment <tutorial-installation>`.


Create a new PHP Laravel project
--------------------------------

On the Control Panel, create a new project selecting:

* *Python*: ``PHP``
* *Project type*: ``Laravel``

..  admonition:: Beta phase constraint

    Your project *must* be:

    * assigned to an Organisation in the Control Panel
    * configured to use an :ref:`external Git repository <configure-version-control>`

    otherwise the Control Panel will not handle it correctly.

Other options can be left on their default settings.


Set up the project locally
--------------------------

List your cloud projects::

   divio project list

Identify the slug of the project you created in the previous step, and use this with the ``divio project setup``
command, for example::

   divio project setup my-tutorial-project

Various processes will unfold, taking a few minutes (see :ref:`build-process` for a description of them).


Start the project
-----------------

``cd`` into the newly-created project directory, where you will find your new Laravel project.

Run the post-installation routines, such as migrations - this may take a few minutes::

    docker-compose run --rm web php /app/divio/setup.php

Then, start the project with ``docker-compose up``:

..  code-block:: bash

    ➜  docker-compose up
    Starting laravel-flavours-example_db_1 ... done
    Starting laravel-flavours-example_web_1 ... done
    Attaching to laravel-flavours-example_db_1, laravel-flavours-example_web_1
    db_1   | LOG:  database system is ready to accept connections
    db_1   | LOG:  autovacuum launcher started
    web_1  | Laravel development server started: <http://0.0.0.0:80>

Once up and running, you will be able to open the project in a web browser on port 8000 (i.e. at ``localhost:8000``).
