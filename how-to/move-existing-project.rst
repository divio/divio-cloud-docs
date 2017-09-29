.. _use-git:


Moving an existing project to Divio Cloud
=========================================

General project setup
---------------------

Create a new project in the Divio Control Panel. You'll need to make some choices for it:

* What software do you want installed automatically? You can select plain Django, Django plus django CMS (the default) or Django plus Wagtail.
* Select the Boilerplate you want to use. Several are available, with different built-in frontend components to work with. Select the Blank Boilerplate if you prefer to set up and manage your site's frontend starting from scratch.

Important: Do not start a deployment yet, we’ll cover that later.

The next step is to select the correct Django version (and if applicable, the django CMS versions) by going to the “Manage Addons” menu and choosing “Configure” for the related package/Addon (e.g. “[System] Divio Django). On the next screen, click on “Change version” and pick the required package.

After these Addons are properly configured, switch to the Command Line Client (the easiest way is to use Divio App for that) and set up a local copy of the project::

    divio project setup <your-project-slug>

Integrating your existing code base and workflow
------------------------------------------------

If you’re not sure about the project slug (or would just like to see a handy cheat sheet for the “Divio Shell” application), see the “Local Development” section on the Control Panel. You can also find the command including the correct project slug in the Divio App:

Integrating your project is quite easy and consists in the following steps:

* Open the requirements.in file inside your project folder and add the required packages (see also http://pip.readthedocs.io/en/1.1/requirements.html).
* Copy the application code and templates into the project folder (Git repository)
* Open settings.py and change it according to your needs (adapting INSTALLED_APPS/, MIDDLEWARE_CLASSES and other custom variables etc.)
* If applicable, add further Git remote repositories to your project (e.g. in case you have your projects hosted on GitHub or Bitbucket, see also https://help.github.com/articles/adding-a-remote/ or https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)

Importing databases
-------------------

Divio Cloud projects use PostgreSQL as a database management system (DBMS). To transfer your existing Postgres data dumps into the Divio Cloud project, the commands to do so could look like following example::

    docker exec <container_id> dropdb -U postgres db --if-exists
    docker exec <container_id> createdb -U postgres db
    docker exec <container_id> psql -U postgres --dbname=db -c "CREATE EXTENSION IF NOT EXISTS hstore"
    docker exec -i <container_id> psql -U postgres --dbname db < /path/to/dump

If you were using a different DBMS like MySQL before, there are multiple options to convert them to a Postgres compatible dataset. Our recommendation is to use a conversion script like https://github.com/lanyrd/mysql-postgresql-converter - but you can also try to export the data to a JSON file (via “manage.py dumpdata”) and then load it back into the new database with “manage.py loaddata”. Note that <container_id> is usually something like: projectslug_db (if you’re unsure, open the docker-compose.yaml file and check.

See the following resources which explain the steps in more detail:

https://github.com/lanyrd/mysql-postgresql-converter
https://wiki.postgresql.org/wiki/Converting_from_other_Databases_to_PostgreSQL
https://www.calazan.com/migrating-django-app-from-mysql-to-postgresql/

After the data is loaded, please make sure that python manage.py migrate works fine and test the website locally.

Media files
-----------

Static files are placed inside the static folder in your project directory (and need to be added to the Git repository).

Media files can be put into project_directory/data/media and are not part of the Git repository. These files need to be uploaded using the following command::

    divio project push media

As soon as you have finished all tests and confirmed that the project works locally, the last step is to push the changes to Divio Cloud.

Syncing changes to the Divio Cloud (Test) Server

For that, simply go through the following steps:

* Git-Commit all changes and Git-Push to Divio Cloud (git@git.divio.com)
* Upload the database to Divio Cloud by using::

    divio project push db

* Deploy the project (either via Control Panel or using)::

    divio project deploy
