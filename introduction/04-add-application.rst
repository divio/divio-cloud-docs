.. _tutorial-add-applications:

Make changes and deploy them
===================================

Next, we're going to install a new package, `Django Axes <https://github.com/jazzband/django-axes>`_, into the project
(Django Axes keeps track of log-in attempts). Then we'll test it and deploy it to the cloud.


.. _tutorial-add-requirements:

Install a package
-----------------

To be used in a containerised system, packages must be built onto the image, otherwise the next time a container is
launched, the package will not be there. The image is built by the Dockerfile, and in our Dockerfile for Django
projects, this includes an instruction to process the project's ``requirements.in`` file with Pip. This is where the
package needs to be added. Add::

    django-axes==3.0.3

at the end of the ``requirements.in`` file. It's important to pin dependencies to a particular version this way; it
helps ensure that we don't run into unwanted surprises if the package is updated, and the new version introduces an
incompatibility.

Now you can build the project again::

    docker-compose build


Configure the Django settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django Axes requires that it be listed in the project's ``INSTALLED_APPS``, in ``settings.py``. Open ``settings.py``.
You'll find the lines::

    import aldryn_addons.settings
    aldryn_addons.settings.load(locals())

This project uses the optional Aldryn Addons system, which makes it possible for projects to configure themselves. For
example, you can can find all the configuration that the Aldryn Django does for Django settings in
``addons/aldryn-django/aldryn_config.py``. You don't have to use this system, but it makes development much faster, as
it takes care of all the settings that would otherwise need to be managed correctly for the different cloud
environments as well as the local environment.

The lines above load all those settings into the ``settings`` module. A good way to see what settings are applied is
via Django's ``diffsettings`` command::

   docker-compose run web python manage.py diffsettings

As you can see, a number of ``INSTALLED_APPS`` are already defined, so we can add ``axes`` to the list:

..  code-block:: python
    :emphasize-lines: 4

    # all Django settings can be altered here

    INSTALLED_APPS.extend([
        "axes",
    ])

..  admonition:: A note for experienced Djangonauts

    This project set-up, and the way we handle settings, may strike experienced Django users as unusual.

    It's important to bear in mind that it's just one way of handling settings in a Django project on Divio. Use of
    Aldryn Django and the whole Aldryn Addons system is wholly optional; if you prefer to manage settings manually,
    that will work just as well.

    One advantage of this way of doing it is that it declutters the ``settings.py file``, removing
    deployment-related values that are better handled via environment variables, and also provides a guarantee that
    settings for database, media and so on will always be correct - Aldryn Django's ``aldryn_config.py`` will set them
    appropriately for each environment, including the local development environment, and also appropriately at each
    stage of the build/deployment process.

    Even if you later plan to use your one preferred set-up, for the purposes of this tutorial it's strongly
    recommended to continue with the way Aldryn Django does it.


Run migrations
--------------

Django Axes introduces new database tables, so we need to run migrations::

    docker-compose run web python manage.py migrate

(As you have probably noticed, we can run all the usual Django management commands, but because we need to run them
inside the containerised environment, we precede each one with ``docker-compose run web``.)


Check the project
--------------------

If you launch the project again with ``docker-compose up`` you'll find Django Axes in the admin:

.. image:: /images/axes.png
   :alt: 'Django Axes in the admin'
   :width: 663

Test it by attempting to log in to the Django admin with an incorrect password.


Deploy to the cloud
-------------------

If you are satisfied with your work, you can deploy it to the cloud.

We made changes to two files (``requirements.in``, ``settings.py``). So::

    git add .
    git commit -m "Added Django Axes"
    git push

On the project Dashboard, you will see that your new commit is listed as *1 Undeployed commit*. You can deploy this
using the Control Panel, or by running::

    divio project deploy

When it has finished deploying, you should check the Test server to see that all is as expected. Once you're satisfied
that it works correctly, you can deploy the Live server too::

    divio project deploy live

This completes the basic cycle of project creation, development and deployment.
