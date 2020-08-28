.. _tutorial-django-services:

Add and configure services
===================================

Your Django application is now running in the cloud as well as locally, but it can't do anything useful until it is
attached to basic services, such as the database and media storage. A blank Divio project type is created without any
services, so these will need to be attached manually.

..  important::

    For this part of the tutorial you will need to be opted-in to Beta features on the Divio Control Panel. You can do
    this in your `account settings <https://control.divio.com/account/contact/>`_.


Database
--------------------------------

Create the database
~~~~~~~~~~~~~~~~~~~~

For the cloud environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the project's :ref:`Services <services>` view, add a PostgreSQL database. When you next deploy, or if you manually
select *Provision* from the services options menu, it will be provisioned for the project (you need to do one of those
now).

.. image:: /images/intro-services.png
   :alt: 'The Services view'
   :class: 'main-visual'


Locally
^^^^^^^^^^^^

For development purposes when working locally, we should also have a database. It's not so easy to set up the right
version of Postgres locally, especially when working with different projects, and as a result many Django developers
content themselves with using SQLite locally, because it's an easy-to-use default. However, it's much better to use the
same database in development as you do in deployment, and Docker Compose can take care of this for you too. Edit your
``docker-compose.yml`` to add some new lines:

..  code-block:: YAML
    :emphasize-lines: 16-

    version: "2"

    services:

      web:
        # the application's web service (container) will use an image based on our Dockerfile
        build: "."
        # Map the internal port 80 to port 8000 on the host
        ports:
          - "8000:80"
        # Map the host directory to app (which allows us to see and edit files inside the container)
        volumes:
          - ".:/app:rw"
        # The default command to run when launching the container
        command: python manage.py runserver 0.0.0.0:80
        # the URL 'postgres' will point to the application's db service
        links:
          - "db:postgres"

      db:
        # the application's web service will use an off-the-shelf image
        image: postgres:9.6-alpine
        environment:
          POSTGRES_DB: "db"
          POSTGRES_HOST_AUTH_METHOD: "trust"
        volumes:
          - ".:/app:rw"

The next time you launch the application locally, it will include a Postgres database running in a ``db`` container.


Configure database access using an environment variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration for application services is `stored in environment variables, following the Twelve-Factor model
<https://www.12factor.net/config>`_. These variables will need to be parsed by the application. For the database the
values are provided via an environment variable named ``DEFAULT_DATABASE_DSN``, a *Data Source Name*, in the general
form::

    scheme://username:password@host:port/path?query#fragment

The variables are provided in the cloud environments as soon as the service is provisioned. We should add a variable
to the local environment too. The easiest way to do this is again with the help of ``docker-compose.yml``.

First, create a new file called ``.env-local``, and add the variable to it:

..  code-block:: text

    DEFAULT_DATABASE_DSN=postgres://postgres@postgres:5432/db

If you're familiar with Postgres, you'll recognise its default user and port in the URL.

Then add a new line to the ``web`` section in ``docker-compose.yml`` to tell it where it should find the variables for
the environment it creates:

..  code-block:: YAML
    :emphasize-lines: 5

      web:
        [...]
        links:
          - "db:postgres"
        env_file: .env-local

Now in every runtime environment, the application will find the correct database connection values; in a cloud
environment, it will find variables provided by the cloud infrastructure, while locally it will use the ones we supply
via ``.env-local``.

Again, this follows the Twelve-Factor principles. `We manage one codebase in version control, and deploy exactly the
same codebase in every deployment <https://www.12factor.net/codebase>`_ - even locally.


Use the environment variable in our settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next task is to connect the application to the database (we will use the Python ``psycopg2`` library) and parse the
URL with connection details (using ``dj_database_url``).

List both libraries in ``requirements.txt``:

..  code-block:: YAML
    :emphasize-lines: 3-

    django==3.1
    uvicorn==0.11.8
    psycopg2==2.8.5
    dj_database_url==0.5.0

Rebuild the image once more to include the new packages.

Then in ``settings.py``, add (replacing the existing ``DATABASES`` setting):

..  code-block:: python

    import os
    import dj_database_url

    [...]

    DEFAULT_DATABASE_DSN = os.environ.get('DEFAULT_DATABASE_DSN')
    DATABASES = {'default': dj_database_url.parse(DEFAULT_DATABASE_DSN)}

We're now in a position to use the database for the first time. The first thing to do is create Django's tables, by
running migrations, and then add an admin user to the database:

..  code-block:: bash

    docker-compose run web python manage.py migrate
    docker-compose run web python manage.py createsuperuser

The next time you run ``docker-compose up``, you'll be able to `log in to the admin <http://127.0.0.1:8000/admin>`_.
(If you don't see the expected styling of the Django admin, it's probably because the site is running with Uvicorn
rather than the runserver - check whether you left the ``command`` line in ``docker-compose.yml`` commented out.)


Deploy your changes
~~~~~~~~~~~~~~~~~~~~

It is worth verifying that the site now runs on the cloud too. Commit the changes you've made:

..  code-block:: bash

    git add docker-compose.yml myapp requirements.txt .env-local
    git commit -m "Added database configuration"
    git push

and deploy:

..  code-block:: bash

    divio project deploy

..  admonition:: Pushing ``.env-local``

    In this case, there is nothing in ``.env-local`` that can't be safely committed, and having the
    ``DEFAULT_DATABASE_DSN`` in there means that if a colleague needs to set up your Divio project, they will that in
    there too, ready to use in their own local environment. However if you were testing functionality that required you
    add a secret key, for example to use some external service, you should take care not to commit that.
    **Configuration secrets should not be committed to code repositories.**

Your local database has been migrated and you have created an admin superuser. In the cloud environment, the Django
database tables have not yet been created, so if you try to access the admin there, you'll naturally get an error:

..  code-block:: text

    ProgrammingError at /admin/login/
    relation "auth_user" does not exist
    LINE 1: ...user"."is_active", "auth_user"."date_joined" FROM "auth_user...

The Divio CLI includes a very convenient way to upload your local database to the cloud. Run:

..  code-block:: bash

    divio project push db

This will push the local database to the cloud Test environment. Once the process has completed, you can refresh the
cloud Test site; you'll be able to log in at ``/admin`` with your admin user credentials.

Similarly, you can push/pull media files, and also specify which cloud environment to target. See the :ref:`local
commands cheatsheet <cheatsheet-project-resource-management>`. A common use-case is to pull live content into the
development environment, so that you can test new development with real data.

You can also execute commands like ``python manage.py migrate`` directly in the cloud environment. Copy the SSH URL
from the Test environment pane in the Control Panel, and use it to open a session directly to a cloud container. Then
run:

..  code-block:: bash

    python manage.py migrate


Serving static files
---------------------

The site's static files need to be handled properly.

As mentioned previously, when using the runserver locally you are able to load the Django admin's CSS at
http://127.0.0.1:8000/static/admin/css/fonts.css; this is because the Django runserver takes care of serving static
files for you. When running with Uvicorn instead of the runserver, the file is not served. If you try to load the same
file from the cloud server, where the ``Dockerfile`` launches the site with Uvicorn, you'll have a similar experience.

When running with a production server like Uvicorn, you need to configure static file serving explicitly. There are
multiple ways to do this, but one very good way to do so on the Divio infrastructure is to use the Python library
`WhiteNoise <http://whitenoise.evans.io>`_. WhiteNoise is designed to work behind Content Delivery Networks and
integrates well with Django.

Add ``whitenoise`` to the ``requirements.in``:

..  code-block:: text

    whitenoise==5.2.0

In ``settings.py``, add it to the list of ``MIDDLEWARE``, after the ``SecurityMiddleware``:

..  code-block:: python
    :emphasize-lines: 3

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        [...]
    ]

And to have it cache and compress static files, and to tell Django where to put collected static files, add:


..  code-block:: python
    :emphasize-lines: 2-3

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

Rebuild the image to have WhiteNoise installed.

To test that Uvicorn and WhiteNoise are serving the static files as expected, comment out the ``command`` line in
``docker-compose.yml`` and set ``DEBUG`` in ``settings.py`` to ``False``.

You will not be able to load the CSS file until you run ``collectstatic`` to have static files collected:

..  code-block:: bash

    docker-compose run web python manage.py collectstatic

Commit and push your changes (first revert the temporary changes to ``docker-compose.yml`` and ``settings.py``).
Deploy the Test environment, and check that static files work as expected there too.


Serving media files
-------------------

Each cloud environment can have its own media storage running on a service such as S3 or MS Azure, and is provided with
a ``DEFAULT_STORAGE_DSN`` variable containing details of how and where files are stored, and the URL from which they
can be retrieved. Django can be configured to access the media storage of each environment by using the
``DEFAULT_STORAGE_DSN`` to determine Django's :setting:`DEFAULT_FILE_STORAGE <django:DEFAULT_FILE_STORAGE>` setting.


Create the media storage
~~~~~~~~~~~~~~~~~~~~~~~~

For the cloud environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the same way that you did for the database earlier, in the project's :ref:`Services <services>` view, add an S3
object storage instance. Once deployed, or if you manually select *Provision* from the services options menu, the
service will be provisioned for the project and the environment variable will be applied.

Locally
^^^^^^^^^^^^

Locally, the most convenient way to work with media files is using local storage. You could use any directory in your
local project, but since the Divio CLI will expect to find media files in ``/data``, we will use that. We will
configure the local set-up so that media files can be:

* stored in ``/data/media``
* retrieved via the URL path ``/media``

We can configure the storage system for this with the ``DEFAULT_STORAGE_DSN`` variable in ``.env-local``. Edit
``.env-local``, adding:

..  code-block:: text

    DEFAULT_STORAGE_DSN=file:///data/media/?url=%2Fmedia%2F

For convenience, we should expose the container's ``/data`` directory so you can see the files in it. In
``docker-compose.yml``, add:

..  code-block:: yaml
    :emphasize-lines: 7

    services:

      web:
        [...]
        volumes:
          - ".:/app:rw"
          - "./data:/data:rw"

And since media files should not be committed to the codebase, edit ``.gitignore``:

..  code-block:: text
    :emphasize-lines: 3

    # Divio
    [...]
    /data


Use the environment variable in our settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next task is to configure Django's ``DEFAULT_FILE_STORAGE`` setting. We need Django to parse the
``DEFAULT_STORAGE_DSN`` variable that contains the connection details and select the appropriate backend accordingly.
For this, we'll use the ``django_storage_url`` library, which needs to be added to ``requirements.txt``. We also need to install ``boto3``, the Python storage backend that will handle files in the project's S3 cloud storage:

..  code-block:: YAML

    django_storage_url==0.5.0
    boto3==1.14.49

Rebuild the image once more to include the new package.

Then in ``settings.py``, add:

..  code-block:: python

    from django_storage_url import dsn_configured_storage_class

    [...]

    # Media files

    # DEFAULT_FILE_STORAGE is configured using DEFAULT_STORAGE_DSN

    # read the setting value from the environment variable
    DEFAULT_STORAGE_DSN = os.environ.get('DEFAULT_STORAGE_DSN')

    # dsn_configured_storage_class() requires the name of the setting
    DefaultStorageClass = dsn_configured_storage_class('DEFAULT_STORAGE_DSN')

    # Django's DEFAULT_FILE_STORAGE requires the class name
    DEFAULT_FILE_STORAGE = 'myapp.settings.DefaultStorageClass'

In brief: we read the ``DEFAULT_STORAGE_DSN`` environment variable value into the setting ``DEFAULT_STORAGE_DSN``. The
``DefaultStorageClass`` is defined using the setting, and then finally that class is used in the
``DEFAULT_FILE_STORAGE`` setting. Now when Django needs to handle media files, it can delegate the task to the
appropriate backend, as defined by the class that ``DEFAULT_FILE_STORAGE`` refers to.

(Note that ``dsn_configured_storage_class()`` and ``DEFAULT_FILE_STORAGE`` both require the *name* of the value, rather
than the value itself, which is why this looks a little long-winded.)


Configure local file storage serving
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using *cloud storage*, media files will be served directly by the external cloud storage service, at the URL
provided in its DSN - nothing further needs to be configured. To serve files from *local* storage, we can use
:ref:`Django's own file serving functionality <django:serving-uploaded-files-in-development>`. It needs to be
configured to recognise the media URL path (``/media/``) and to locate the media root directory of the files
(``/data/media``).

First, set the Django settings ``MEDIA_URL`` and ``MEDIA_ROOT`` to match the values in the ``DEFAULT_STORAGE_DSN``:

..  code-block:: python

    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join('/data/media/')

And then add a new pattern to ``myapp/urls.py``:

..  code-block:: python
    :emphasize-lines: 1-2, 6

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

As the Django documentation notes, this is not for production use, but in any case, it will only work when Django
is in debug mode, so it's ideal for local development.


Test file storage and serving configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a good point at which to test that your local and cloud file storage both work correctly. We'll create a very
simple Django application in the project that saves uploaded files to storage.

Create the new application in the project:

..  code-block:: bash

    docker-compose run web python manage.py startapp uploader

Add a new model to ``uploader/models.py``:

..  code-block:: python
    :emphasize-lines: 3-4

    from django.db import models

    class UploadedFile(models.Model):
        file = models.FileField()

Wire it up to the admin in ``admin.py``:

..  code-block:: python
    :emphasize-lines: 3-5

    from django.contrib import admin

    from uploader.models import UploadedFile

    admin.site.register(UploadedFile)

Add it to ``INSTALLED_APPS`` in ``settings.py``:

..  code-block:: python
    :emphasize-lines: 3

    INSTALLED_APPS = [
        [...]
        'uploader',
    ]

And create and run migrations:

..  code-block:: bash

    docker-compose run web python manage.py makemigrations uploader
    docker-compose run web python manage.py migrate uploader

Now when you start the project again with ``docker-compose up``, you can go to the admin and try uploading a file .

Once you have saved it in the admin, you should be able to verify that it has been saved in the filesystem at
``/data/media``, that Django shows its URL path in ``/media/`` in the admin interface, and finally, that by selecting
the link to the file in the admin it opens correctly in your browser.

You can also check that it will work with the cloud storage values; you can do this locally. Stop the application, and use:

..  code-block:: bash

    divio project env-vars -s test --all --get DEFAULT_STORAGE_DSN

to get the value of the ``DEFAULT_DATABASE_DSN`` from the cloud test environment. (If you don't get a value, check in
the *Services* view of the project that it has been provisioned.) In your ``.env-local``, apply this value as the
``DEFAULT_DATABASE_DSN``. Launch the application once more, and run the test above again, uploading and saving a file.
This time, you should find that the saved file is now served from the external media server.

The final test is to try it all in the cloud. Revert the ``DEFAULT_STORAGE_DSN`` to its local value
(``file:///data/media/?url=%2Fmedia%2F``) and commit your code changes in the usual way.

Then, deploy the changes and push your local media and database to the cloud:

..  code-block:: bash

    divio project deploy
    divio project push media
    divio project push db

You should find all your media and database content in the cloud environment now, and you should be able to use the
admin interface to upload new files too.
