:sequential_nav: both

.. _tutorial-django-deploy:

Deploy your application to the `Divio Cloud <https://www.divio.com>`_
=====================================================================

One further step is required before the application can be deployed to the cloud. Django's :setting:`ALLOWED_HOSTS
<django:ALLOWED_HOSTS>` setting controls the hosts that are allowed to serve the application. When undefined, 
``localhost`` is allowed by default, which will work locally, but not in a cloud deployment.

The quick solution is to amend ``settings.py`` to allow any host:

..  code-block:: python

    ALLOWED_HOSTS = ['*']

Normally, this is not something you would do in production. However it will suffice for now and we will refine it later.

The application is now in a state where it can be deployed to the cloud. All the files that define the application
should be committed and pushed. It's always good to exclude unwanted files from Git *before* you commit them
inadvertently, so add some new patterns to the application's ``.gitignore`` file:

..  code-block:: bash

    # macOS
    .DS_Store
    .DS_Store?
    ._*
    .Spotlight-V100
    .Trashes

    # Python
    *.pyc
    *.pyo
    db.sqlite3

    # Divio
    .divio
    /data.tar.gz

(``.divio`` is used by the Divio CLI to refer to the correct cloud application; ``/data.tar.gz`` is created by the CLI
when pulling a database from the cloud. Neither should be committed to the repository.)

Now it's safe to commit the application files you have been working on:

..  code-block:: bash

    git add .gitignore Dockerfile docker-compose.yml manage.py myapp requirements.txt
    git commit -m "Defined basic application components"
    git push

On the application Dashboard, you will see that your new commit is listed, and that it now reports *3 Undeployed 
commits*. You can deploy the Test environment using the Control Panel, or by running:

..  code-block:: bash

    divio app deploy

Once you have successfully deployed the Test environment, the Control Panel will indicate this in the interface with a
*Last deployment successful* message and the application URL in the Test environment pane will display as a link,
for example ``https://tutorial-project-stage.us.aldryn.io``. Select the link to access the application.


--------------

Your Django application is now running in the cloud as well as locally, but it can't do anything useful until it is
attached to basic services, such as the database and media storage. In the next sections we will take care of:

* database storage
* static asset compilation, storage and serving
* media storage and serving
