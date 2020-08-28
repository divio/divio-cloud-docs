.. _tutorial-django-refinements:

Apply some refinements
===================================

We now have a working application, that functions in multiple environments and takes its configuration for the services
it requires from environment-provided variables.

However, there a number of refinements we can make.


Configure ``ALLOWED_HOSTS``
---------------------------

:ref:`Earlier <tutorial-django-deploy>`, we set :setting:`ALLOWED_HOSTS <django:ALLOWED_HOSTS>` to ``['*']``, which
allows any host to serve the application, for convenience. This isn't ideal - ``ALLOWED_HOSTS`` exists for a reason.

Each client environment is provided with a :ref:`DOMAIN <env-var-domain>` environment variable, and (if the project
uses multiple domains) a :ref:`DOMAIN_ALIASES <env-var-domain-aliases>` environment variable, which can be used to
configure ``ALLOWED_HOSTS``. You can see what environment variables have been set by using:

..  code-block::bash

    divio project env-vars --all

(Use the ``-s live`` option to see the variables for the Live environment.)

We can use these environment variables to populate ``ALLOWED_HOSTS``, and only use ``['*']`` if it would otherwise be
empty - which would be the case only in the local development environment. Edit the settings file again:

..  code-block:: python

    DIVIO_DOMAIN = os.environ.get('DOMAIN', '*')

    DIVIO_DOMAIN_ALIASES = [
        d.strip()
        for d in os.environ.get('DOMAIN_ALIASES', '').split(',')
        if d.strip()
    ]

    ALLOWED_HOSTS = [DIVIO_DOMAIN] + DIVIO_DOMAIN_ALIASES


Configure ``SECRET_KEY``
------------------------

Django's secret key is hard-coded in our settings and committed to the repository. This is all right locally, but not
in production. However, since each cloud environment is provided with its own randomised ``SECRET_KEY`` variable, we
can use that by changing ``settings.py`` to use:

..  code-block:: python

    SECRET_KEY = os.environ.get('SECRET_KEY', 'c(oz0r_18@)5ojt(fnom)r)^)gb5zt519$$%5jnz)gpyzxn-4+')


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
    CMD uvicorn --host=0.0.0.0 --port=80 myapp.asgi:application

However, if you try to run ``docker-compose build`` now, you'll run into an error. During the build process, Docker has
no access to environment variables - including the ones it's expecting to use to define settings such as ``DATABASES``.
This is how it should be: building a Docker image should not be dependent upon any particular environment conditions.

The solution is a to build a fallback into the Django settings by editing the line that determines the
``DEFAULT_DATABASE_DSN`` setting:

..  code-block:: python

    DEFAULT_DATABASE_DSN = os.environ.get('DEFAULT_DATABASE_DSN', 'sqlite://:memory:')

Now when no ``DEFAULT_DATABASE_DSN`` can be found in the environment, Django will happily use a dummy backend instead.
You can test it by building again.

The ``/staticfiles`` directory no longer needs to be a part of the repository. Remove it:

..  code-block:: bash

    git rm -r staticfiles

and add ``/staticfiles`` to ``.gitignore``.

Commit and push the code changes, and run a deployment to check results. From now on, even if you add new applications
with their own static files, or change the static files in existing applications, they will be collected automatically
on deployment.

..  admonition:: Static files, locally

    When working locally, the static files collected by Docker inside the container will be *overwritten*, because of

    ..  code-block:: yaml

        volumes:
          - ".:/app:rw"

    as soon as Docker Compose is invoked. This doesn't matter when you're using Django in debug mode, because it
    will take care of static files for you, but if you're trying to work with ``DEBUG = False`` and need your
    static files to be served, you'll have to re-create them by running:

    ..  code-block:: bash

        docker-compose run web python manage.py collectstatic


Improve the way we set ``MEDIA_ROOT`` and ``MEDIA_URL``
---------------------------------------------------------

There is something unsatisfactory about the way we hard-code these settings:

..  code-block:: python

    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join('/data/media/')

If we ever decide to use a different value for ``DEFAULT_STORAGE_DSN`` locally, we'll also have to update the settings
file. Since we already have the ``DEFAULT_STORAGE_DSN`` value in settings, we should extract the values we need from
that. We can do that with the `furl <https://github.com/gruns/furl>`_ library (which is what Django Storage URL does
internally).

..  code-block:: python

    from furl import furl

    [...]

    MEDIA_URL = furl(DEFAULT_STORAGE_DSN).args.get('url')
    MEDIA_ROOT = os.path.join(str(furl(DEFAULT_STORAGE_DSN).path))


Set ``DEBUG`` using an environment variable
--------------------------------------------

``DEBUG`` is also hard-coded into the project code. This is not a good idea. We want to be sure that we don't
inadvertently go into production with ``DEBUG = True``. So, let's make it default to ``False``, and overwrite it only
where we need it to be True. First, in ``.env-local``:

..  code-block:: text

    DJANGO_DEBUG=True
    DJANGO_TEMPLATE_DEBUG=True

and change the risky ``DEBUG = True`` in ``settings.py``:

..  code-block:: python

    DEBUG = os.environ.get('DJANGO_DEBUG', False)
    TEMPLATE_DEBUG = os.environ.get('DJANGO_TEMPLATE_DEBUG', False)

Your code can now be deployed with more confidence; only if the environment explicitly declares that Django can run in
debug mode will it do that.

Test locally; commit your changes once again, and redeploy and test on the cloud.

Run ``divio project deploy live``, and test it in the Live environment too.

You should be able to verify that exactly the same codebase runs in multiple different environments, configuring itself
appropriately and using the different resources and services available in each.

-------------------


This completes the basic cycle of project creation, development and deployment, and how to integrate multiple cloud
services into an application. You should now be familiar with the fundamental concepts and tools involved.

Other sections of the documentation expand upon these topics. The :ref:`how-to guides <how-to>` in particular cover
many common operations. And if there's something you're looking for but can't find, please contact Divio support.

