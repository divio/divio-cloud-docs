.. _tutorial-set-up:

Create a new project
====================

In this section we will create and deploy a new project in the Control Panel.


Set up a project in the Cloud
-----------------------------

Create your account
~~~~~~~~~~~~~~~~~~~

A Divio account is free to set up and use indefinitely. Create your
account on the Divio  `Control Panel <https://control.divio.com/>`_, or
log in if you already have one.


.. _tutorial-create-project:

Create the project
~~~~~~~~~~~~~~~~~~

In the Divio Control Panel, `create a new project <https://control.divio.com/control/project/create/>`_.

Any web application in any language can run on Divio, as long as there is nothing that prevents its being Dockerised.
However for convenience we also provide a number of ready-to-go project types for applications built in Java, PHP, Node
and other languages (and the list is growing).

This tutorial uses `Django <https://www.djangoproject.com/>`_, the most popular Python web application framework, for
an example project. You don't need to know Django or Python, or have them installed on your system, and the principles
covered by the tutorial will apply to any other development stack.

Select the following options for your project (other options can be left on their default settings):

* *Python*: ``Python 3.x``
* *Project type*: ``Django``

..  admonition:: Django 2.2

    At the time of writing, version 2.2 is `Django's Long-Term Support release
    <https://www.djangoproject.com/download/#supported-versions>`_, and is
    guaranteed support until at least April 2022. This is the version currently
    selected by default in Divio projects.

Divio projects use Git for code management. We provide a Git server that your projects will use by default; you can
also choose to :ref:`use another Git service if you prefer <configure-version-control>`. For this tutorial, use our
Git server.

Hit **Create**. (You may be asked to select a subscription for the project; select the free *Developer* plan if so.)

It takes a few moments to create the project. During this process, the Control Panel defines the Docker image for your
application by adding commits to its repository, assembling its :ref:`Dockerfile <dockerfile-reference>` and other
files.



Deploy the project
~~~~~~~~~~~~~~~~~~

Once the project has been created, use the **Deploy** button to deploy the Test server.

The deployment process first builds the Docker image from the ``Dockerfile``, and then launches a Docker container from
the image. The container environment will include automatically-configured environment variables for connections to
services such as the database, media storage and so on.

Typically, this takes a minute or so.


Project environments
^^^^^^^^^^^^^^^^^^^^

.. image:: /images/intro-dashboard.png
   :alt: 'Project Dashboard'
   :class: 'main-visual'


Your project has two independent server environments, Test and Live. The Test and Live servers have their own services,
and unique environment variables to configure access to them. They can be deployed independently, and can also :ref:`be
configured to track different Git branches <custom-tracking-branches>`.


Log in to the project
~~~~~~~~~~~~~~~~~~~~~

Once you have successfully deployed the Test server, the Control Panel will indicate a *Last deployment successful at
...* message, and the project URL in the Test server pane will display as link, e.g.
https://my-project-stage.us.aldryn.io.

Open the link to access the project. Since this is your own project, you can use our :ref:`single-sign-on
<authentication>` to log in by selecting **Log in with Divio**.

You'll see the familiar Django admin for a new project.

.. image:: /images/intro-django-admin.png
   :alt: 'Django admin'
   :class: 'main-visual'

It doesn't do anything interesting yet - but it's up and running and ready to start working on.


About deployment
-------------------------

Any time new changes to the project code are committed to its repository, the Control Panel will indicate this with a
message showing the number of undeployed commits for each of its server environments.

New code and configuration changes applied via the Control Panel (to subscriptions, cron jobs, environment variable,
domains or other settings) will not take effect on either server environment until it is deployed once again.

If for whatever reason a deployment fails, there will be no down-time - the containers that are currently running will
continue running, and the failing changes will not be deployed.


Explore the Dashboard
---------------------

The Divio project Dashboard provides you with access to useful controls and information for the project. They are
fairly self-explanatory and at this stage you don't need to interact with any of them, but it's worth familiarising
yourself with what's available.
