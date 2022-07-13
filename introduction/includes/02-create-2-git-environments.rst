..  This include is used by:

    * django-02-create-project.rst
    * aldryn-django-02-create-project
    * laravel-02-create-project.rst
    * wagtail-02-create-project.rst


`Divio <https://www.divio.com>`_ Applications use Git for code management. We provide a Git server that your 
Applications will use by default; you can also choose to 
:ref:`use another Git service if you prefer <configure-version-control>`. For this tutorial, use our Git server.

Hit **Continue**, then select the free *Developer* plan for this Application (the Developer plan is fully-featured and
provides all you need to work on an application up to the point of putting it into production).

It takes a few moments to create the Application. During this process, the Control Panel defines the basic Application 
files for your application by adding commits to its repository. This could include assembling its :ref:`Dockerfile
<dockerfile-reference>` and other files, depending on the Application type.


Application environments
~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: /images/intro-dashboard.png
   :alt: 'Application Dashboard'
   :class: 'main-visual'

Your Application has two independent server environments, *Test* and *Live* . The Test and Live environments have their 
own services, and unique environment variables to configure access to them. They can be deployed independently, and can
also :ref:`be configured to track different Git branches <custom-tracking-branches>`.
