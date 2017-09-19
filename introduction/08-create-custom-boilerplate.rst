.. _tutorial-create-boilerplate:

Create a custom Boilerplate
===========================

Each Divio Cloud site has a frontend *Boilerplate*, a set of default templates
and static files.

Typically, a Boilerplate will define how the Django templates are structured
and will commit the project to certain frontend frameworks and tools.

We provide :ref:`a number of default Boilerplates <about-boilerplates>`, suited
to different purposes.

However, you may have your own preferences for frontend setups (tooling,
configuration, and so on) for your sites, especially if you or your team build
many of them.

You could build this tooling into each site on each occasion, but it could save
you a great deal of time to define it just once, in a custom Boilerplate, and
then use it on each occasion.

In this section of the tutorial we will build a custom Boilerplate.


Set up a new project to work in
-------------------------------

In order to give you a meaningful context in which to learn about creating
Boilerplates, you need a project with a suitable application. This section sets
up a new project, with a simple Polls application.

..  admonition:: Or, use your own application

    If you'd prefer to do this in a project using one of your own applications,
    that's even better. You'll need to make some minor adjustments to some of
    the steps, but if you already have a suitable project ready, you can go
    straight to the :ref:`add-foundation-frontend` section.


Create a new project
~~~~~~~~~~~~~~~~~~~~

..  note::

    See the more detailed tutorial, :ref:`tutorial-set-up`, if you are not
    already familiar with these steps.

In the Divio Cloud Control Panel, create a new ``Django``-type project, based
on ``Python 3.x`` and the ``Blank Boilerplate``.

Deploy the Test server.


Replicate it locally
~~~~~~~~~~~~~~~~~~~~

List your cloud projects::

    divio project list

Set up the new project locally, for example::

    divio project setup my-boilerplate-project

And in the project directory, start it with::

    divio project up


.. _add-simple-application:

Add a simple application
~~~~~~~~~~~~~~~~~~~~~~~~

..  note::

    Refer to :ref:`tutorial-add-applications` if this is new to you.

In the new project, run:

..  code-block:: bash

    git clone git@github.com:divio/django-polls.git

(or use ``git clone https://github.com/divio/django-polls.git`` if you can't
use the SSH URL) and put the inner ``polls`` application directory at the root
of your project, for example by running::

    mv django-polls/polls .

to install a simple polls application in the project.

In the project's ``settings.py``, add the polls application:

..  code-block:: python
    :emphasize-lines: 2

    INSTALLED_APPS.extend([
        "polls",
    ])

Migrate the database:

..  code-block:: bash

    docker-compose run --rm web python manage.py migrate

And check that you can see the polls application in the admin.

Edit ``urls.py`` to add the URLconf for the ``polls`` application:

..  code-block:: python
    :emphasize-lines: 2

    urlpatterns = [
        url(r'^polls/', include('polls.urls', namespace='polls')),
    ] + aldryn_addons.urls.patterns() + i18n_patterns(
        # add your own i18n patterns here
        *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!

Then check that you can create polls with questions, and see them listed at
http://localhost:8000/polls/.

..  image:: /images/polls-default.png
    :alt: The polls application with a Question and Choices

You now have working project in which to implement the frontend.


.. _add-foundation-frontend:

Add a Foundation frontend
-------------------------

We'll create a Boilerplate that sets up new projects with the popular
`Foundation <http://foundation.zurb.com>`_ frontend.


Add the Foundation files
~~~~~~~~~~~~~~~~~~~~~~~~

From the `Foundation download page
<http://foundation.zurb.com/sites/download.html/>`_, select the
complete Foundation 6 package.

Copy its ``index.html`` file into your project's (**not** the polls
application's) ``templates`` directory, and rename it to ``base.html`` (this
is just a good Django convention).

Copy the ``css`` and ``js`` directories to the ``static`` directory of the
project.

Adapt the *generic Foundation* template (``base.html``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we'll get to work on the templates, starting from the bottom (the
Foundation ``base.html`` template).

``base.html`` contains:

..  code-block:: HTML

    <link rel="stylesheet" href="css/foundation.css">
    <link rel="stylesheet" href="css/app.css">

These need to use the correct static file locations; add ``{% load staticfiles
%}`` to the top of the template, and change the lines thus:

..  code-block:: HTML

    <link rel="stylesheet" href="{% static 'css/foundation.css' %}">
    <link rel="stylesheet" href="{% static 'css/app.css' %}">

And then you will need to work through the template, modifying lines and adding
in hooks for Django content and functionality. This will also involve removing
all the welcome text. Amended lines are highlighted:

..  code-block:: Django
    :emphasize-lines: 1, 3, 7-15, 17-24

    {% load staticfiles %}
    <!doctype html>
    <html class="no-js" lang="{{ LANGUAGE_CODE }}" dir="ltr">
      <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        {% block meta_viewport %}
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {% endblock %}
        {% block extra_meta %}{% endblock %}
        <title>{% block title %}{% endblock %}</title>
        <link rel="stylesheet" href="{% static 'css/foundation.css' %}">
        <link rel="stylesheet" href="{% static 'css/app.css' %}">
        {% block extra_link %}{% endblock %}
        {% block extra_head %}{% endblock %}
      </head>
      <body {% block body_attributes %}{% endblock %}>
        {% block body %}{% endblock %}
        {% block body_script %}
          <script src="js/vendor/jquery.js"></script>
          <script src="js/vendor/what-input.js"></script>
          <script src="js/vendor/foundation.js"></script>
          <script src="js/app.js"></script>
        {% endblock %}
      </body>
    </html>

This template should be generic enough that it can be used right away in any
Foundation-based project.


Add a *project-specific* template (``main.html``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now add a ``main.html`` template, next to the new Foundation ``base.html``. It
extends ``base.html``, and supplies some material that you would expect to be
specific to each project. Highlighted lines show where we hook into the
``base.html``.

..  code-block:: HTML
    :emphasize-lines: 1, 3, 5, 9, 13

    {% extends "base.html" %}

    {% block title %}Project title{% endblock %}

    {% block body %}
      <div class="grid-container">
      <div class="grid-x grid-padding-x">
        <div class="large-12 cell">
          {% block application_content %}{% endblock %}
        </div>
      </div>
      </div>
    {% endblock %}


Add an *application-specific* template (``polls/base.html``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The polls application knows nothing of the new templates we have created.

If you look at the polls application, you will see that each of its view
templates (the index view, the detail view and so on) extend its own, minimal
``polls/templates/polls/base.html`` file, which contains nothing but:

..  code-block:: HTML

    {% block polls_content %}{% endblock %}

What we want is to wire up the polls application to the new templates in our
project. We could do this by modifying ``polls/base.html`` to extend
``main.html``, but when using a reusable application such as polls, it's always
better to *override* it than to *modify* it).

In the *project's* ``templates`` directory, add a ``polls`` directory and
inside that add a ``base.html``:

..  code-block:: HTML

    {% extends "main.html" %}

    {% block title %}Django Polls{% endblock %}

    {% block application_content %}
      {% block polls_content %}{% endblock %}
    {% endblock %}

This will override the existing ``base.html`` belong to the application, and
allow the ``{% block polls_content %}`` from the views' templates to be
inserted into the ``{% block application_content %}`` of the project template.

Check that it all works. Your polls application should now have basic Foundation
styling in all its views:

..  image:: /images/polls-foundation.png
    :alt: The polls application with a Foundation frontend


About the chain of extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This might seem like an overly-complex series of ``{% extend %}`` template tags,
but the template structure sets a good standard and will help us later on
when we need to reuse it.

+-----------------------------+----------------------------------------+---------------------------+
| Level                       | Location                               | Notes                     |
+=============================+========================================+===========================+
|                             | ``polls/templates/polls/index.html``   |                           |
+                             +----------------------------------------+                           +
| application view templates  | ``polls/templates/polls/detail.html``  | extend ↓                  |
+                             +----------------------------------------+                           +
|                             | ``polls/templates/polls/results.html`` |                           |
+-----------------------------+----------------------------------------+---------------------------+
| application base template   | ``polls/templates/polls/base.html``    | not used, overridden by ↓ |
+-----------------------------+----------------------------------------+---------------------------+
| application base template   | ``templates/polls/base.html``          | overrides ↑, extends ↓    |
+-----------------------------+----------------------------------------+---------------------------+
| project-specific template   |``templates/main.html``                 | extends ↓                 |
+-----------------------------+----------------------------------------+---------------------------+
| generic Foundation template | ``templates/base.html``                |                           |
+-----------------------------+----------------------------------------+---------------------------+


You don't have to remember all this, or even understand it fully right now -
but it's here if you need to refer to it.

**Why this structure?**

Keeping the generic Foundation template free of any project-specific material
will make it easier to use in other projects. Keeping application-specific
material out of project templates will make it easier to use them with other
applications.


.. _create-boilerplate-package:

Create the Boilerplate package
------------------------------

We now have enough for a basic, working Boilerplate. It provides:

* a ``base.html`` Foundation template that is replete with ``{% block %}``
  template tags, allowing it to be extended in a vast variety of ways
* a ``main.html`` template that the project developer can customise
* Foundation's static CSS and JS assets.

For convenience, we will create a new directory called ``tutorial-boilerplate``
in the root of the project, and **copy** those items to it, so that the
directory looks like this::

    tutorial-boilerplate/
        static/
            css/
            js/
        templates/
            base.html
            main.html


The ``boilerplate.json`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``boilerplate.json`` in ``tutorial-boilerplate``:

..  code-block:: JSON

    {
        "package-name": "tutorial-boilerplate",
        "templates": [],
        "identifier": "foundation6",
        "version": "0.0.1"
    }

* The ``package-name`` is whatever you'd like to call it - however, it must
  be unique on the Divio Cloud system.
* ``templates`` are only required for Boilerplates intended to be used with
  django CMS.
* ``identifier`` is a namespace, that will allow applications that are
  Boilerplate-aware to build in support for particular Boilerplates into their
  own frontend code. (An example of this is `Aldryn News & Blog
  <https://github.com/aldryn/aldryn-newsblog>`_ - compare its `Bootstrap
  frontend
  <https://github.com/aldryn/aldryn-newsblog/tree/master/aldryn_newsblog/boilerp
  lates/bootstrap3>`_ with its `'plain' templates
  <https://github.com/aldryn/aldryn-newsblog/tree/master/aldryn_newsblog/templat
  es/aldryn_newsblog>`_.)
* The ``version`` should be updated appropriately, both for your own
  convenience and to help manage the versions that you upload to the Control
  Panel.

Run the ``boilerplate validate`` command to check that the ``boilerplate.json``
is in order::

    ➜  divio boilerplate validate
    Boilerplate is valid!


Add a licence file
~~~~~~~~~~~~~~~~~~

Create a file called ``LICENSE`` (note US English spelling):

    Copyright <YEAR> <COPYRIGHT HOLDER>

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

This is required before your Boilerplate can be uploaded.

This is a `2-Clause BSD "Simplified" License
<https://opensource.org/licenses/BSD-2-Clause>`_.


Create a Boilerplate on Divio Cloud
-----------------------------------

Register your Boilerplate
~~~~~~~~~~~~~~~~~~~~~~~~~

Go to `your Boilerplates on the Divio Cloud website
<https://control.divio.com/account/my-boilerplates/>`_, and hit **Add custom
Boilerplate**.

On the next page, enter its *Name* and *Package name* - the latter must match
the ``package-name`` in the ``boilerplate.json``, then **Create Boilerplate**.


Upload your Boilerplate
~~~~~~~~~~~~~~~~~~~~~~~

Now you need to upload your Boilerplate.

In the :ref:`tutorial-boilerplate directory you created earlier
<create-boilerplate-package>`, run the ``boilerplate upload`` command::

    ➜  divio boilerplate upload
    The following files will be included in your boilerplate and uploaded to
    the Divio Cloud:
    ./LICENSE
    ./static/css/app.css
    ./static/css/foundation.css
    ./static/css/foundation.min.css
    ./static/js/app.js
    ./static/js/vendor/foundation.js
    ./static/js/vendor/foundation.min.js
    ./static/js/vendor/jquery.js
    ./static/js/vendor/what-input.js
    ./templates/base.html
    ./templates/main.html
    Are you sure you want to continue and upload the preceding (#10) files to
    the Divio Cloud? [Y/n]: y
    ok

Your Boilerplate is now on the Divio Cloud.

Refresh the Boilerplate's *General settings* page, and you will see that the
*Identifier* field now reflects the ``foundation6`` value in the
``boilerplate.json``.

Add a description, for example:

    A simple Foundation Boilerplate for testing.

You should also set the *License* field to ``2-Clause BSD "Simplified"
License``, and **Save settings** once more.

Your Boilerplate is now available to use in your projects.


Test your Boilerplate
---------------------

Create another new project, just like you did earlier. This time, however,
instead of selecting the ``Blank Boilerplate``, select *Custom*, and you should
find your new Boilerplate listed there - so create your project based on that.

Set the project up locally, and check that it contains the files you expect::

    static/
        css/
        js/
    templates/
        base.html
        main.html

Then proceed to :ref:`add the polls application to it as you did earlier
<add-simple-application>`.

Finally, you'll need to wire the polls application up the project templates, so
that the polls application's ``base.html`` will be overridden by one that is
aware of of our Boilerplate's ``main.html``. Once again, in the project's
``templates`` directory, add a ``polls`` directory and inside that add a
``base.html``:

..  code-block:: HTML

    {% extends "main.html" %}

    {% block title %}Django Polls{% endblock %}

    {% block application_content %}
      {% block polls_content %}{% endblock %}
    {% endblock %}

And now when you run the project and view your polls, you should see that the
Foundation frontend is at work.


Update your Boilerplate
-----------------------

..  hint::

    It would be wise to turn your ``tutorial-boilerplate`` directory into a Git
    repository, so you can track changes in it. (This is what we do with
    :ref:`the provided Divio Cloud Boilerplates <about-boilerplates>`).


When you make changes to your Boilerplate, increment its ``version`` in the
``boilerplate.json`` and upload it to the Control Panel by running the
``boilerplate upload`` command on the new version.

..  important::

    When a Boilerplate is updated, it doesn't affect any projects that were
    built using an earlier version of it. A Boilerplate is only used once on a
    project, at the moment of its creation.

    Any updates will need to be merged manually into existing projects.

You'll find its *Versions* listed on its page in the Control Panel.
