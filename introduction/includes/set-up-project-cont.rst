Divio projects use Git for code management. We provide a Git server that your projects will use by default; you can
also choose to :ref:`use another Git service if you prefer <configure-version-control>`. For this tutorial, use our
Git server.

Hit **Create**. (You may be asked to select a subscription for the project; select the free *Developer* plan if so.)

It takes a few moments to create the project. During this process, the Control Panel defines the Docker image for your
application by adding commits to its repository, assembling its :ref:`Dockerfile <dockerfile-reference>` and other
files.


Project environments
~~~~~~~~~~~~~~~~~~~~

.. image:: /images/intro-dashboard.png
   :alt: 'Project Dashboard'
   :class: 'main-visual'


Your project has two independent server environments, *Test* and *Live* . The Test and Live environments have their own
services, and unique environment variables to configure access to them. They can be deployed independently, and can
also :ref:`be configured to track different Git branches <custom-tracking-branches>`.


Deploy the project
~~~~~~~~~~~~~~~~~~

Once the project has been fully created, use the **Deploy** button to deploy the Test server.

The deployment process first builds the Docker image from the ``Dockerfile``, and then launches a Docker container from
the image. The container environment will include automatically-configured environment variables for connections to
services such as the database, media storage and so on.

Typically, this takes a minute or so.


Open the Test environment website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have successfully deployed the Test environment, the Control Panel will indicate a *Last deployment successful
at ...* message, and the project URL in the Test environment pane will display as a link, for example
``https://tutorial-project-stage.us.aldryn.io``. Open the link to access the project.
