.. _tutorial-migrate-project:

Migrate a project to Divio Cloud
================================

In this tutorial you will take an existing Django project and port it to Divio Cloud.

The project (`The Opinions Company <https://github.com/divio/the-opinions-company>`_) complete with
custom applications, database content, media files and styling is contained in a GitHub repository.


Set the project up locally
--------------------------

Clone the project, and cd into the directory::

    git clone git@github.com:divio/the-opinions-company.git
    cd the-opinions-company

Create and activate a virtual environment::

    python3.6 -m venv env
    source env/bin/activate

Install the project's dependencies into the virtual environment::

    pip install -r requirements.txt

Run migrations to create the empty database tables::

    python manage.py migrate

Load the database content from the ``database.json`` file::

    python manage.py loaddata database.json

Start the runserver::

    python manage.py runserver

You can now open the site at http://localhost:8000. The username and password are
``admin``/``admin``. Check that you can log in and use the site and its admin.


Dump database to a JSON file (if required)
------------------------------------------

If you have made some additional changes to the database that you'd like to load into the Divio
Cloud project, you can dump them with::

    python manage.py dumpdata --natural-foreign --natural-primary --indent 4 > database.json


Migrate to Divio Cloud
----------------------

Create a new Divio Cloud project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On the Divio Cloud control panel, `create a new project
<https://control.divio.com/control/project/create/>`_, with the options:

* Python 3
* django CMS
* Blank boilerplate

Once the new project has been provisioned, see its *Addons* view:

* django CMS: ensure that the version of django CMS installed matches that in your project (3.5.3)
* django CMS Bootstrap 4: *install* django CMS Bootstrap 4 (version 1.0.1)


Set the project up locally
~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the ``divio project setup`` command (the exact command can be found in the *Local development*
view).


Check the Divio project's dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Paste the entire contents of your original project's ``requirements.txt`` file into the
``requirements.in`` of the Divio project, after the auto-generated section.

We now have to scan through this line-by-line, to check for conflicts. In the *Addons* view for the
project in the Control Panel, select *Installed addons*, and for each line you have added,
cross-check to see whether it has already been included.

You will find that most are already present, and you'll also be able to see that in them listed in
the auto-generated section in the file.

As you confirm that each one is present, you can remove the corresponding line that you copied over
- it's no longer required. For example (note that our projects, versions
and dependencies all change over time, so the actual results you see may be slightly different)::

    django-cms>=3.5,<3.6                # No need to add this manually

    # django CMS plugins and addons

    djangocms-text-ckeditor>=3.6.0      #
    djangocms-link>=2.1                 #
    djangocms-style>=2.0                # You can expect all of these to be
    djangocms-googlemap>=1.1            # present already amongst the addons
    djangocms-snippet>=2.0              # included in the project, so there
    djangocms-video>=2.0                # is probably no need for them to be
    djangocms-file>=2.0,<3.0            # added manually to the requirements.in
    djangocms-picture>=2.0,<3.0         # file.
    django-filer>=1.3                   #
    djangocms-bootstrap4==1.0.0         #

Some may or may not be explicitly listed amongst the project's addons, but can be found in the
`setup.py of django CMS <https://github.com/divio/django-cms/blob/develop/setup.py>`_ (make sure
you're looking at the right version), so once again, they won't need to be included, though you
should still check that the version numbers are compatible.

::

    # Django dependencies (specified in django CMS's setup.py)

    Django<2.0                          # Already installed by Aldryn Django

    django-classy-tags>=0.7             # These dependencies are specifed by
    django-sekizai>=0.9                 # django CMS, so will be installed
    django-treebeard>=4.0,<5.0          # automatically anyway.
    djangocms-admin-style>=1.2,<1.3     #

The original ``requirements.txt`` file lists some further Python dependencies. You may recogise
some of them (and that, for example, ``easy_thumbnails`` is a dependency of Django Filer). However
if you need to, you canc check the Divio Project to see what has already been installed, with
``docker-compose run --rm web pip freeze``. All the following should already be present, and do not
need to be listed manually::

    # Python dependencies

    html5lib>=0.999999,<0.99999999      #
    Pillow>=3.0                         # Should all be present in the Divio
    pytz                                # Project's environment.
    six                                 #
    easy_thumbnails                     #

Finally, there is the Polls application, installed via pip from GitHub::

    # polls

    -e git+git@github.com:divio/django-polls.git#egg=django-polls

This *will* need to be specified in the ``requirements.in`` file. However, the ``-e`` (editable)
option makes little sense in this context, and :ref:`our pip setup cannot handle requirements in
this format <vcs-protocol-support>`. Instead, you need to provide the URL of an archive, in this
case::

    https://github.com/divio/django-polls/archive/b89f59b933113b82c49062830912c42a8fc15c77.zip

We use the commit, because otherwise :ref:`our pip system could cache an older version
<pinning-dependencies>`.

And that is the only requirement you need to add manually to the ``requirements.in`` file.


Copy the ``polls_cms_integration`` application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``polls_cms_integration`` application is in the project folder of the original project. This
needs to be copied to the same place in the Divio project.


Test the build
~~~~~~~~~~~~~~

You can now test whether the project will build::

    docker-compose build web

If you run into an error, you most likely either have a dependency version conflict, or the
``collectstatic`` command in the ``Dockerfile`` cannot run, because a required dependency is
missing. This will need to be resolved before you can proceed.


Populate the ``INSTALLED_APPS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the original project, all the ``INSTALLED_APPS`` are listed manually. In a Divio project,
most of them will be added automatically by the addons. You need to ensure that your Divio
project includes all those in the original project.

Add the following to the end of the ``settings.py`` of each project::

    for app in INSTALLED_APPS:
        print(app)

For the original project, run::

    python manage.py shell

and for the Divio project run::

    docker-compose run --rm web python manage.py shell

In each case, copy the list of applications into a file, order the lines alphabetcially and save
the file. Now run a ``diff`` on the two files::

    diff original-installed-apps divio-installed-apps

In the output you will see lines starting with:

* ``>`` - an application present in the Divio project, but not in the original
* ``<`` - an application listed in the original, but not in the Divio project

In the first case, no action is required. In the second case, you will see that::

    < polls
    < polls_cms_integration

both need to be added manually (``the_opinions_company`` is also listed, but this is just the
project name and doesn't need to be added).

List::

    'polls_cms_integration',
    'polls',

in the::

    INSTALLED_APPS.extend([
        [...]
    ])

section so that they will be added.


Transfer other settings
~~~~~~~~~~~~~~~~~~~~~~~

Your original project's settings need to be transferred to the Divio project. Settings in Divio
projects can be handled in multiple ways:

* via an addon's configuration form, as defined by its ``aldryn_config.py`` file
* as environment variables
* as plain old settings in ``settings.py``

The best way to maintain the ``CMS_TEMPLATES`` setting in a Divio project is via the form. In the
local version of the project, the form values are stored in
``addons/aldryn-djangocms/settings.json``.

However, for now it's easiest to include the setting in the ``settings.py`` file temporarily, so
add::

    CMS_TEMPLATES = (
        ('content.html', 'Content'),
    )

(Later we will do this another way.)


Prepare the Postgres database of the Divio project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The database has so far been migrated, but that's all.

..  admonition:: Have you touched the Divio project database?

    If you have done anything else to this database, you will need to restore it to its newly-migrated
    state::

        docker ps  # list the containers to find its id

        docker exec <database container id> dropdb -U postgres db --if-exists  # drop the database
        docker exec <database container id> createdb -U postgres db  # create the database
        docker exec <database container id> psql -U postgres --dbname=db -c "CREATE EXTENSION IF NOT EXISTS hstore"  # add the hstore extension
        docker-compose run --rm web python manage.py migrate  # migrate the database

Now you can import the dumped JSON data. Copy ``database.json`` over from the original project, and
run::

    docker-compose run --rm web python manage.py loaddata database.json


Copy site templates
~~~~~~~~~~~~~~~~~~~

Next, we need to Copy the two templates ``base.html`` and ``content.html`` template from
``the_opinions_company/templates`` in the original project to ``templates`` in the Divio project.


Copy static files
~~~~~~~~~~~~~~~~~

Copy all the folders in ``the_opinions_company/static`` to ``static``.


Copy media
~~~~~~~~~~

Copy ``media`` into the ``data`` directory of the Divio project.


Start the runserver
~~~~~~~~~~~~~~~~~~~

::

    docker-compose up


Check the site
~~~~~~~~~~~~~~

Once again, check that the site works as expected.

Now you're ready to push your work to the Cloud.


Push your changes to the Divio Cloud environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Code
^^^^

Earlier, we added::

    CMS_TEMPLATES = (
        ('content.html', 'Content'),
    )

to the ``settings.py``. That was only a temporary expedient - remove that now, because you don't
want to push that.

Instead, in your project in the Control Panel, go to the *Addons* > *Aldryn django CMS* >
*Configure*, and in the *CMS Templates* field apply::

    [["content.html", "Content"]]

Now you can push the rest of your code. Run ``git status`` to see what has been changed. ``git
add`` the changes you want to push::

    git add requirements.in settings.py polls_cms_integration static templates

And::

    git commit -m "Set up The Opinions Company as a Divio project"

Finally::

    git pull  # merge the changes you made in the Control Panel
    git push origin develop  # push local changes


Database
^^^^^^^^

Push the database::

    divio project push db


Media
^^^^^

And the media files::

    divio project push media


Deploy the new Divio Cloud project
----------------------------------

On the Control Panel, you see that there are now a number of undeployed commits, representing the
work you have done.

You can hit **Deploy** on the Control Panel, or run::

    divio project deploy

And that's it! Your project is now running in the Cloud.
