.. _tutorial-add-applications:

Add new applications to the project
===================================

..  admonition:: This tutorial assumes your project uses Django 1.11

    At the time of writing, version 1.11 is `Django's Long-Term Support release
    <https://www.djangoproject.com/download/#supported-versions>`_, and is
    guaranteed support until at least April 2020.

    If you use a different version, you will need to modify some of the code
    examples and version numbers of packages mentioned.


..  note::

    In this section, we'll assume your project is already running
    (``docker-compose up web``) and that you are in your own shell, not at the
    ``bash`` prompt in a container.


Add a package to the project directory
--------------------------------------

The simplest way to add a new Django application to a project is by placing it
in the project directory, so it's on the Python path. We'll use `a version of
the Polls application <https://github.com/divio/django-polls>`_ that's part of
the Django tutorial.

Download the application (tip: open a second terminal shell so you can leave
the project running):

..  code-block:: bash

    git clone git@github.com:divio/django-polls.git

..  note::

    The URL above requires that you have `provided your public key to GitHub
    <https://help.github.com/articles/connecting-to-github-with-ssh/>`_.

    Otherwise, use ``https://github.com/divio/django-polls.git``.

And put the inner ``polls`` application directory at the root of your project
(you can do this with: ``mv django-polls/polls .``).


Configure the project
---------------------

Configure settings
^^^^^^^^^^^^^^^^^^

Edit ``settings.py`` to include the ``polls`` application:

..  code-block:: python
    :emphasize-lines: 2

    INSTALLED_APPS.extend([
        "polls",
    ])

This ``settings.py`` already includes ``INSTALLED_APPS`` that have been
configured by applications in the project - here we are simply extending it
with new ones.


Configure URLs
^^^^^^^^^^^^^^

Edit ``urls.py`` to add the URLconf for the ``polls`` application:

..  code-block:: python
    :emphasize-lines: 2

    urlpatterns = [
        url(r'^polls/', include('polls.urls', namespace='polls')),
    ] + aldryn_addons.urls.patterns() + i18n_patterns(
        # add your own i18n patterns here
        *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!


Migrate the database
--------------------

Run:

..  code-block:: bash

    docker-compose run web python manage.py migrate

You will see the migrations being applied::

    Running migrations:
      Rendering model states... DONE
      Applying polls.0001_initial... OK

And when that has completed, open the project again in your browser:

..  code-block:: bash

    divio project open

You should see the new polls application in the admin:

..  image:: /images/polls-admin.png
    :alt: The polls application appears in the admin

Deploy the project
------------------

Push your changes
^^^^^^^^^^^^^^^^^

If it works locally it should work on the Cloud, so let's push the changes to
the Test server and deploy there.

First, add the change:

..  code-block:: bash

    git add settings.py urls.py polls

Commit them:

..  code-block:: bash

    git commit -m "Added polls application"

And push to the Divio Cloud Git server:

..  code-block:: bash

    git push origin develop

..  note::

    The Control Panel will display your undeployed commits, and even a diff
    for each one.


Deploy the Test server
^^^^^^^^^^^^^^^^^^^^^^

..  code-block:: bash

    divio project deploy test

And check the site on the Test server:

..  code-block:: bash

    divio project test

Optionally, if you made some local changes to the database (perhaps you added
some polls), you can push the database to the local server too, with:

..  code-block:: bash

    divio project push db

(You'll need to redeploy to see the results.)


Add a package via pip
---------------------

Often, you want to add a reusable, pip-installable application. For this
example, we'll use `Django Axes <https://github.com/jazzband/django-axes>`_,
a simple package that keeps access logs (and failed login attempts) for a site.

Add the package
^^^^^^^^^^^^^^^

Add ``django-axes==2.3.2`` (it's always sensible to specify a version number in
requirements) to the project's ``requirements.in``:

..  code-block:: python
    :emphasize-lines: 4

    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    [...]
    # </INSTALLED_ADDONS>
    django-axes==2.3.2

(Make sure that it's *outside* the automatically generated ``#
<INSTALLED_ADDONS>`` section.)

Rebuild the project
^^^^^^^^^^^^^^^^^^^

The project now needs to be rebuilt, so that Django Axes is installed:

..  code-block:: bash

    docker-compose build web

Configure settings
^^^^^^^^^^^^^^^^^^

In the ``settings.py``, add ``axes`` to ``INSTALLED_APPS``:

..  code-block:: python
    :emphasize-lines: 3

    INSTALLED_APPS.extend([
        "polls",
        "axes",
    ])

(Note that this application doesn't need an entry in ``urls.py``, because it
only uses the admin).

Run migrations
^^^^^^^^^^^^^^

Now the database needs to be migrated once again for the new application:

..  code-block:: bash

    docker-compose run web python manage.py migrate

Check that it has installed as expected (Django Axes will show its records in
the admin).

Deploy to the Cloud
^^^^^^^^^^^^^^^^^^^

To deploy this to the Test server, push your changes, and deploy once more:

..  code-block:: bash

    git add settings.py requirements.in
    git commit -m "Added Django Axes"
    git push origin develop
    divio project deploy test
