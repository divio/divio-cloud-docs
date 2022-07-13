:sequential_nav: prev

.. _tutorial-django-refinements:

Apply some refinements
===================================

We now have a working application, that functions in multiple environments and takes its configuration for the services
it requires from environment-provided variables.

However, there are a number of refinements we can make.


Set ``DEBUG`` using an environment variable
--------------------------------------------

``DEBUG`` is hard-coded into the application code. This is not a good idea. We want to be sure that we don't 
inadvertently go into production with ``DEBUG = True``. So, let's make it default to ``False``, and overwrite it only 
where we need it to be True. First, in ``.env-local``:

..  code-block:: text

    DJANGO_DEBUG=True

and change the risky ``DEBUG = True`` in ``settings.py``:

..  code-block:: python

    DEBUG = os.environ.get('DJANGO_DEBUG') == "True"

Your code can now be deployed with more confidence; only if the environment explicitly declares that Django can run in
debug mode will it do that (any other value for the environment variables than ``True`` will evaluate to ``False`` in
the settings).

Test locally; commit your changes once again, and redeploy and test on the cloud.


Configure ``ALLOWED_HOSTS``
---------------------------

:ref:`Earlier <tutorial-django-deploy>`, we set :setting:`ALLOWED_HOSTS <django:ALLOWED_HOSTS>` to ``['*']``, which
allows any host to serve the application, for convenience. This isn't ideal - ``ALLOWED_HOSTS`` exists to
:ref:`mitigate fake Host header attacks <django:host-headers-virtual-hosting>`, and even if this risk doesn't apply in
Divio's cloud hosting environments, it's a bad idea to bake in configuration to your code that could be unsafe in
others. It's better if we can restrict ``ALLOWED_HOSTS`` to the right domains.

Each Divio cloud environment is provided with a :ref:`DOMAIN <env-var-domain>` environment variable, and (if the
application uses multiple domains) a :ref:`DOMAIN_ALIASES <env-var-domain-aliases>` environment variable. These can be used to configure ``ALLOWED_HOSTS``. You can see what environment variables have been set by using:

..  code-block:: bash

    divio app env-vars --all

(Use the ``-s live`` option to see the variables for the Live environment.)

We can use these environment variables to populate ``ALLOWED_HOSTS``. Edit the settings file again:

..  code-block:: python

    DIVIO_DOMAIN = os.environ.get('DOMAIN', '')

    DIVIO_DOMAIN_ALIASES = [
        d.strip()
        for d in os.environ.get('DOMAIN_ALIASES', '').split(',')
        if d.strip()
    ]
    DIVIO_DOMAIN_REDIRECTS = [
        d.strip()
        for d in os.environ.get('DOMAIN_REDIRECTS', '').split(',')
        if d.strip()
    ]

    ALLOWED_HOSTS = [DIVIO_DOMAIN] + DIVIO_DOMAIN_ALIASES + DIVIO_DOMAIN_REDIRECTS
    

Now, ``ALLOWED_HOSTS`` will always contain only the domains specified by the environment variables. On the cloud, these
are provided automatically; for the local development environment, we need to add the right ones to ``.env-local``:

..  code-block:: text

    DOMAIN_ALIASES=localhost, 127.0.0.1


Configure ``SECRET_KEY``
------------------------

Django's secret key is hard-coded in our settings and committed to the repository. This is all right locally, but not
in production. However, since each cloud environment is provided with its own randomised :ref:`SECRET_KEY
<env-var-secret-key>` variable, we can use that by changing ``settings.py`` to use that (also providing a fall-back):

..  code-block:: python

    SECRET_KEY = os.environ.get('SECRET_KEY', '<a string of random characters>')


Configure SSL redirects
-----------------------

In production, it's almost always better to redirect to HTTPS, when the server supports it. However, we don't want it
when running locally. So, in settings, we will default to redirecting:

..  code-block:: python

    # Redirect to HTTPS by default, unless explicitly disabled
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT') != "False"

And in the ``.env-local``, to disable it:

..  code-block:: text

    SECURE_SSL_REDIRECT=False


Add ``collectstatic`` to the build
---------------------------------------

At the moment, we need to run ``python manage.py collectstatic`` manually (and then commit the static files to the
repository).

This is a well-defined, repeatable task that is not really worthy of a human's attention. It would be much more elegant
to have it executed automatically. We can do this using the ``Dockerfile``:

..  code-block:: Dockerfile
    :emphasize-lines: 2

    RUN pip install -r requirements.txt
    RUN python manage.py collectstatic --noinput
    CMD uwsgi --module=myapp.wsgi --http=0.0.0.0:80

However, if you try to run ``docker-compose build`` now, you'll run into an error. During the build process, Docker has
no access to environment variables - including the ones it's expecting to use to define settings such as ``DATABASES``.
This is how it should be: building a Docker image should not be dependent upon any particular environment conditions.

The solution is to build a fallback into the Django settings by editing the line that determines the
``DATABASE_URL`` setting:

..  code-block:: python

    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite://:memory:')

Now when no ``DATABASE_URL`` can be found in the environment, Django will happily use a dummy backend instead.
You can test it by building again.

The ``/staticfiles`` directory no longer needs to be a part of the repository. Remove it:

..  code-block:: bash

    git rm -r staticfiles

and add ``/staticfiles`` to ``.gitignore``.

Commit and push the code changes, and run a deployment to check results. From now on, even if you add new applications
with their own static files, or change the static files in existing applications, they will be collected automatically
on deployment.

..  admonition:: Serving static files, locally

    When working locally, the static files collected by Docker inside the container will be *overwritten*, because of

    ..  code-block:: yaml

        volumes:
          - ".:/app:rw"

    as soon as Docker Compose is invoked. This doesn't matter when you're using Django in debug mode, because it
    will take care of static files for you, but if you're trying to work with ``DEBUG = False`` and need your
    static files to be served, you'll have to re-create them by running:

    ..  code-block:: bash

        docker-compose run web python manage.py collectstatic


-------------------


This completes the basic cycle of application creation, development and deployment, and how to integrate multiple cloud
services into an application. You should now be familiar with the fundamental concepts and tools involved.

Other sections of the documentation expand upon these topics. The :ref:`how-to guides <how-to>` in particular cover
many common operations. And if there's something you're looking for but can't find, please contact 
`Divio <https://www.divio.com>`_ `support <https://www.divio.com/support/>`_.

