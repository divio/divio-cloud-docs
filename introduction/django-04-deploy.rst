:sequential_nav: both

.. _tutorial-django-deploy:

Deploy your application to the cloud
====================================

One further step is required before the application can be deployed to the cloud. Django's :setting:`ALLOWED_HOSTS
<django:ALLOWED_HOSTS>` setting controls the hosts that are allowed to serve the project. When undefined, ``localhost``
is allowed by default, which will work locally, but not in a cloud deployment.

The simple solution is to amend ``settings.py``, with:

..  code-block:: python

    ALLOWED_HOSTS = ['*']

It's a crude solution, but we will refine it later.

The application is now in a state where it can be deployed to the cloud. All the files that define the application
should be committed and pushed. It's always nice to exclude unwanted files from Git *before* you commit them
inadvertently, so add some new patterns to the project's ``.gitignore`` file:

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

(``.divio`` is used by the Divio CLI to refer to the correct cloud project; ``/data.tar.gz`` is created by the CLI
when pulling a database from the cloud. Neither should be committed to the repository.)

Now it's safe to commit the project files you have been working on:

..  code-block:: bash

    git add .gitignore Dockerfile docker-compose.yml manage.py myapp requirements.txt
    git commit -m "Defined basic application components"
    git push

On the project Dashboard, you will see that your new commit is listed, and that it now reports *3 Undeployed commits*.
You can deploy the Test environment using the Control Panel, or by running:

..  code-block:: bash

    divio project deploy

Once you have successfully deployed the Test environment, the Control Panel will indicate this in the interface with a
*Last deployment successful* message and the project URL in the Test environment pane will display as a link,
for example ``https://tutorial-project-stage.us.aldryn.io``. Select the link to access the project.


--------------

The application is now running in a cloud deployment. However, more needs to be done. Core concerns of a web
application will typically include

* database storage
* static asset compilation, storage and serving
* media storage and serving

:ref:`The next section <tutorial-django-services>` will take care of those.
