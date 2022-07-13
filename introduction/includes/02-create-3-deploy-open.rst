..  This include is used by:

    * aldryn-django-02-create-project
    * laravel-02-create-project.rst
    * wagtail-02-create-project.rst


Deploy the application
~~~~~~~~~~~~~~~~~~~~~~

Once the application has been fully created, use the **Deploy** button to deploy the Test server.

The deployment process first builds the Docker image from the ``Dockerfile``, and then launches a Docker container from
the image. The container environment will include automatically-configured environment variables for connections to
services such as the database, media storage and so on.

Typically, this takes a minute or so.


Open the Test environment website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have successfully deployed the Test environment, the Control Panel will indicate this in the interface with a
*Last deployment successful at ...* message and the application URL in the Test environment pane will display as a link,
for example ``https://tutorial-project-stage.us.aldryn.io``. Select the link to access the application.
