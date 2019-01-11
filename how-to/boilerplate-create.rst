.. _how-to-create-boilerplate:

How to create a boilerplate
===============================================

..  seealso::

    * :ref:`Create a custom boilerplate <tutorial-create-boilerplate>` tutorial
    * :ref:`about-boilerplates`


To create a boilerplate, you need to be working in an actual project. An ideal way to start is
by cloning an existing project that has a set-up that corresponds closely to the one you're
planning to make reusable by packaging it as a boilerplate.


Create a boilerplate directory
------------------------------

Create a new directory in the root of your project, called something like ``boilerplate-files``.


Ensure HTML, CSS and JS files are reusable
------------------------------------------

Your boilerplate will typically provide HTML templates, CSS and JavaScript files to the projects
that use it.

Ensure that these are in the right places, and are generic enough that they can be readily resused.
It's no good if for example templates contain project-specific material. Any project-specific
templating should be moved *out* of the template you will be including in the boilerplate, and
instead Django ``{% block %}`` template tags for template inheritance should be added.

Similarly, you should ensure that CSS and JS files are suitably generic.




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