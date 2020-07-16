Make changes and deploy them
===================================

Now you have a working Django Wagtail installation. It includes the ``Page`` model, from ``wagtail.core.models``, that
typically you would extend to include your own fields.

This process is described in the `Wagtail tutorial
<https://docs.wagtail.io/en/stable/getting_started/tutorial.html#extend-the-homepage-model>`_, and adds a ``home``
application to the Django project that adds a new page type. We'll run through the steps here.


Add a new ``home`` application
------------------------------

You'll notice that we use ``docker-compose run web`` a lot here, to execute familiar Django commands inside the
project's Docker environment.

Create the application
~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: bash

    docker-compose run web python manage.py startapp home

Edit its ``models.py`` to add a new HomePage model with a ``body`` field:

..  code-block:: python

    from django.db import models

    from wagtail.core.models import Page
    from wagtail.core.fields import RichTextField
    from wagtail.admin.edit_handlers import FieldPanel


    class HomePage(Page):
        body = RichTextField(blank=True)

        content_panels = Page.content_panels + [
            FieldPanel('body', classname="full"),
        ]


Configure the Django settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``home`` needs to be listed in the project's ``INSTALLED_APPS``, in ``settings.py``. Add ``home`` to the
list:

..  code-block:: python
    :emphasize-lines: 4

    # all Django settings can be altered here

    INSTALLED_APPS.extend([
        "home",
    ])


..  include:: includes/04-add-application-django-01.rst


Create migrations and migrate the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: bash

    docker-compose run web python manage.py makemigrations home
    docker-compose run web python manage.py migrate home


Add templates to the project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Project-level ``base.html`` template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``templates``, add a ``base.html``:

..  code-block:: html

    <!DOCTYPE html>

        <head>
            <title>{{ self.title }}</title>
        </head>

        <body>
            <h1>{% block page_title %}{% endblock %}</h1>

            {% block content %}{% endblock %}
        </body>

    </html>


Application-level templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``home/templates/home/home_page.html``:

..  code-block:: html

   {% extends "base.html" %}

   {% load wagtailcore_tags %}

   {% block page_title %}{{ page.title }}{% endblock %}

   {% block content %}{{ page.body|richtext }}{% endblock %}


Add a page in the Wagtail admin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the usual Wagtail way, add a new page under *Home*, and ensure that in *Settings* > *Sites*, the default Site is
attached to it.


Deploy to the cloud
-------------------

If you are satisfied with your work, you can deploy it to the cloud.

We made changes ``settings.py``, added the ``home`` application and some ``templates``. So:

..  code-block:: bash

    git add .
    git commit -m "Added Home application"
    git push

On the project Dashboard, you will see that your new commit is listed as *1 Undeployed commit*. You can deploy this
using the Control Panel, or by running:

..  code-block:: bash

    divio project deploy

When it has finished deploying, you should check the Test server to see that all is as expected. Once you're satisfied
that it works correctly, you can deploy the Live server too:

..  code-block:: bash

    divio project deploy live


..  include:: includes/04-add-application-push-01.rst


Install a package from pip
---------------------------

Next, we're going to install a new package, `Django Axes <https://github.com/jazzband/django-axes>`_, into the project
(Django Axes keeps track of log-in attempts). Then we'll test it and deploy it to the cloud.

To be used in a containerised system, packages must be built onto the image, otherwise the next time a container is
launched, the package will not be there. The image is built by the ``Dockerfile``, and in our ``Dockerfile`` for Django
projects, this includes an instruction to process the project's ``requirements.in`` file with Pip. This is where the
package needs to be added. Open ``requirements.in`` and at the end of it add a new line::

    django-axes==3.0.3

It's important to pin dependencies to a particular version this way; it helps ensure that we don't run into unwanted
surprises if the package is updated, and the new version introduces an incompatibility.

Now you can build the project again by running::

    docker-compose build


Configure the Django settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As before, add the application (``axes``) to the settings:

..  code-block:: python
    :emphasize-lines: 5

    # all Django settings can be altered here

    INSTALLED_APPS.extend([
        [...]
        "axes",
    ])


Run migrations
~~~~~~~~~~~~~~

..  code-block:: bash

    docker-compose run web python manage.py migrate axes


Check the project
~~~~~~~~~~~~~~~~~

If you launch the project again with ``docker-compose up`` you'll find Django Axes in the admin at ``/django-admin``:

.. image:: /images/axes.png
  :alt: 'Django Axes in the admin'
  :width: 663

Test it by attempting to log in to the Django admin with an incorrect password.


Deploy again
~~~~~~~~~~~~

Once more, you need to:

* commit the changes
* push them
* deploy them on the cloud


More complex configuration
--------------------------

See :ref:`tutorial-application-configuration` from the basic Django tutorial pathway. This includes some further
configuration examples that it is good to know about.


Where to go next?
------------------

This completes the basic cycle of project creation, development and deployment; you should now be familiar with the
fundamental concepts and tools involved.

Other sections of the documentation expand upon them. The :ref:`how-to guides <how-to>` in particular cover many
common operations. And if there's something you're looking for but can't find, please contact Divio support.
