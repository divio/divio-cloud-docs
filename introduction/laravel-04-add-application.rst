.. _tutorial-flavours-php-add-application:

Make changes and deploy them
===================================

Make a change
-------------

We'll make a simple change to the project code. Find the file ``resources/views/welcome.blade.php``, which is responsible for the Laravel welcome page, and adjust the line controlling the background colour, for example:

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

To deploy your changes to the Test server, push your changes, and run a deployment command:

..  code-block:: bash

    git add composer.json app.flavour .flavour
    git commit -m "Added laravel-responsecache"
    git push origin master

On the project Dashboard, you will see that your new commit is listed as *1 Undeployed commit*. You can deploy this
using the Control Panel, or by running:

..  code-block:: bash

    divio project deploy

When it has finished deploying, you should check the Test server to see that all is as expected. Once you're satisfied
that it works correctly, you can deploy the Live server too:

..  code-block:: bash

    divio project deploy live

------------

This is about a simple change as its possible to make and deploy, but it helps illustrate the workflow and the
development/deployment cycle. In the next section we'll work through some more sophisticated steps.
