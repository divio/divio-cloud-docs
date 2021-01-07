:sequential_nav: both

.. _tutorial-django-media:

Add and configure media storage
================================

Each cloud environment can have its own media storage running on a service such as S3 or MS Azure, and is provided with
a :ref:`DEFAULT_STORAGE_DSN <env-var-storage-dsn>` variable containing details of how and where files are stored, and
the URL from which they can be retrieved. Django can be configured to access the media storage of each environment by
using the ``DEFAULT_STORAGE_DSN`` to determine Django's :setting:`DEFAULT_FILE_STORAGE <django:DEFAULT_FILE_STORAGE>`
setting.


Create the media storage
-------------------------

For the cloud environments
~~~~~~~~~~~~~~~~~~~~~~~~~~

In the same way that you did for the database earlier, in the project's :ref:`Services <services>` view, add an *Object
storage* instance. This will provide S3 storage for the project. Deploy the environment, or manually select *Provision*
from the services options menu. The service will be provisioned for the project and the environment variable will be
applied.

Locally
~~~~~~~

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
``docker-compose.yml``, add (make sure you're editing the ``web`` service, not ``db``):

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
--------------------------------------------

The next task is to configure Django's ``DEFAULT_FILE_STORAGE`` setting. We need Django to parse the
``DEFAULT_STORAGE_DSN`` variable that contains the connection details and select the appropriate backend accordingly.
For this, we'll use the ``django-storage-url`` library, which needs to be added to ``requirements.txt``. We also need to install ``boto3``, the Python storage backend that will handle files in the project's S3 cloud storage:

..  code-block:: YAML

    django-storage-url==0.5.0
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

In brief:

* We read the ``DEFAULT_STORAGE_DSN`` environment variable value into the setting ``DEFAULT_STORAGE_DSN``.
* The ``DefaultStorageClass`` is defined using the setting.
* Finally that class is used in the ``DEFAULT_FILE_STORAGE`` setting.

Now when Django needs to handle media files, it can delegate the task to the appropriate backend, as defined by the
class that ``DEFAULT_FILE_STORAGE`` refers to.

(Note that ``dsn_configured_storage_class()`` and ``DEFAULT_FILE_STORAGE`` both require the *name* of the value, rather
than the value itself, which is why this looks a little long-winded.)


Configure local file storage serving
--------------------------------------------

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
    :emphasize-lines: 1-2, 8-

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]

    if settings.DEBUG:
        urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))


As the Django documentation notes, this is not for production use, but in any case, it will only work when Django
is in debug mode, so it's ideal for local development.


Test file storage and serving configuration
--------------------------------------------

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


Test local media storage
~~~~~~~~~~~~~~~~~~~~~~~~

Now when you start the project again with ``docker-compose up``, you can go to the admin and try uploading a file .

Once you have saved it in the admin, you should be able to verify that it has been saved in the filesystem at
``/data/media``, that Django shows its URL path in ``/media/`` in the admin interface, and finally, that by selecting
the link to the file in the admin it opens correctly in your browser.


Test cloud media storage
~~~~~~~~~~~~~~~~~~~~~~~~

You can also check that it will work with the cloud storage values, and will actually store and serve files from the S3
object storage instance. You can do this locally. Stop the application, and use:

..  code-block:: bash

    divio project env-vars -s test --all --get DEFAULT_STORAGE_DSN

to get the value of the ``DEFAULT_STORAGE_DSN`` from the cloud test environment. (If you don't get a value, check in
the *Services* view of the project that it has been provisioned.) In your ``.env-local``, *temporarily* apply this
value as the ``DEFAULT_STORAGE_DSN``, replacing the existing one. Launch the application once more, and run the test
above again, uploading and saving a file. This time, you should find that the saved file is now served from the
external media server.

The final test is to try it all in the cloud.

Revert the ``DEFAULT_STORAGE_DSN`` to its local value (``file:///data/media/?url=%2Fmedia%2F``). Now, commit all your
code changes in the usual way and push them.

Finally deploy the changes and push your local media and database to the cloud:

..  code-block:: bash

    divio project deploy
    divio project push media
    divio project push db

You should find all your media and database content in the cloud environment now, and you should be able to use the
admin interface to upload new files too.
