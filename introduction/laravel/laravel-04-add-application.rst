:sequential_nav: both

.. _tutorial-flavours-php-add-application:

Make changes and deploy them
===================================

Make a change
-------------

We'll make a simple change to the application code. Find the file ``resources/views/welcome.blade.php``, which is 
responsible for the Laravel welcome page, and adjust the line controlling the background colour, for example:

..  code-block:: php
    :emphasize-lines: 4

    <!-- Styles -->
    <style>
        html, body {
            background-color: black;
            color: #636b6f;

and reload the page to check that it has taken effect.


Deploy to the Cloud
-------------------

Push your code
~~~~~~~~~~~~~~~~~

To deploy your changes to the Test server, push your changes, and run a deployment command:

..  code-block:: bash

    git add .
    git commit -m "Change background colour of welcome page"
    git push origin master

On the application Dashboard, you will see that your new commit is listed as *1 Undeployed commit*. You can deploy this
using the Control Panel, or by running:

..  code-block:: bash

    divio app deploy

When it has finished deploying, you should check the Test server to see that all is as expected. Once you're satisfied
that it works correctly, you can deploy the Live server too:

..  code-block:: bash

    divio app deploy live


Push the database
~~~~~~~~~~~~~~~~~

Your cloud database hasn't yet been migrated, unlike the local database (which you migrated when you ran the
:ref:`divio/setup.php set-up script <laravel-set-up-script>`). One very useful function of the Divio CLI is ability to
push and pull your database and media storage to and from the cloud environments. Push the database with:

..  code-block:: bash

    divio app push db

This will push the local database to the cloud Test environment. (``divio app push db live`` will do the same for
the Live environment.)

Similarly, you can push/pull media files, and also specify which cloud environment. See the :ref:`local commands
cheatsheet <cheatsheet-project-resource-management>`. A common use-case is to pull live content into the development
environment, so that you can test new development with real data.


------------

This is about a simple change as its possible to make and deploy, but it helps illustrate the workflow and the
development/deployment cycle. In the next section we'll work through some more sophisticated steps.
