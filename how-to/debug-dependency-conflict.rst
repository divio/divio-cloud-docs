.. _debug-dependency-conflict:

How to identify and resolve a dependency conflict
=================================================

Occasionally when running a deployment on the Cloud or building an application locally, the process will fail, with a message like:

..  code-block:: text

    ERROR: Service 'web' failed to build: The command '/bin/sh -c pip-reqs compile
    && pip-reqs resolve && pip install --no-index --no-deps --requirement
    requirements.urls' returned a non-zero code: 1

This tells us that pip ran into problems while processing the application's requirements. Resolving this
requires a little detective work. The good news is that the information you require is provided,
and the process for working through it to find the answer is set out below.


Identify the conflict
---------------------

Looking a little further up the log, we'll see something like (this is just a representative
example):

..  code-block:: text
    :emphasize-lines: 3-4

    found candidate dj-redis-url==0.1.4 (constraint was <any>)
    found candidate dj-static==0.0.6 (constraint was <any>)
    Could not find a version that matches Django<1.11,<2.0,<2.1,<2.2,==1.8.18,>=1.11,
    >=1.6,>=1.8
    Tried: 1.1.3, 1.1.4, 1.2, 1.2.1, 1.2.2 [etc]

The highlighted line tells us what the problem is: pip could not find a version of Django that
matched **all** the listed constraints - naturally, because it's impossible to have a version of
Django that **equals** 1.8.18, **is less than** 1.11, and **is also greater than or equal to** 1.11.

So, between them, the packages being installed in the application have some mutually incompatible
requirements. This can often be caused by *unpinned dependencies*, when a package is listed as a
requirement without specifying a version.

In this example, we can see that the conflict is between Django ``<1.11`` and ``==1.8.18`` on one
hand, and ``>=1.11`` on the other.

In your case, the packages and version numbers affected will be different, but the principle is the
same.

..  admonition:: But I didn't change anything in my application!

    Because of the way pip works, even if you don't change anything at all in your application, simply
    rebuilding it can pull in new packages, if they were unpinned. Whenever the application is built,
    it will select the latest versions of unpinned packages, and those versions may introduce new,
    incompatible, requirements of their own.


Identify the problem requirement
--------------------------------

The question now is to ascertain *which* of these requirements we will accept and which we will
change.

In example above, we have a strong clue. The most firmly-pinned of these requirements is
``==1.8.18``. All the others are more loosely pinned. That suggests that Django 1.8.18 has been
specified for a good reason.

In this example, searching through the log for ``Django==1.8.18`` will reveal::

    adding Django==1.8.18
      from aldryn-django==1.8.18.1

which means that the requirement for Django 1.8.18 has come from the Aldryn Django addon. So,
while that version of the addon is specified, it's the requirement for ``Django>=1.11`` that is
the problem.

There is a second clue in the log that indicates which requirement is the problem. As well as being
incompatible with ``Django==1.8.18``, the requirement for ``Django>=1.11`` is *also* incompatible
with another requirement: ``Django<1.11``. A requirement that conflicts with multiple other
requirements is most likely to be the one we should address.

So in this case, we now know that the ``Django>=1.11`` requirement is the one to tackle.


Identify where the requirement comes from
-----------------------------------------

The next question is: where does the requirement for ``Django>=1.11`` come from? A search in the
log for the string ``>=1.11`` will reveal this - for example (again, your own results will be
different, but you will see something in this pattern)::

    adding django<2.2,>=1.11
      from djangocms-attributes-field==0.4.0

meaning that ``djangocms-attributes-field==0.4.0`` wants to install a version of Django greater
than or equal to 1.11 but less than 2.2.

We can quickly verify this by checking the `setup.py in the 0.4.0 branch of the
djangocms-attributes-field repository
<https://github.com/divio/djangocms-attributes-field/blob/0.4.0/setup.py>`_, where the incompatible
requirement is introduced (it's not present in `earlier versions
<https://github.com/divio/djangocms-attributes-field/blob/0.3.0/setup.py#L27-L29>`_).

Now we know that djangocms-attributes-field 0.4.0 has an incompatible Django requirement, so
specifying a version lower than 0.4.0 (``djangocms-attributes-field<0.4.0``) should solve the
problem.

Before doing that, it is wise to check what packages require djangocms-attributes-field, and what
versions. So repeat the process above: search in the log for ``djangocms-attributes-field``. You
might find, for example::

     adding djangocms-attributes-field>=0.1.1
       from djangocms-file==2.0.2
            djangocms-link==2.1.2
            djangocms-picture==2.0.5
            djangocms-style==2.0.2
            djangocms-video==2.0.3

meaning that all those packages have specified a version of djangocms-attributes-field greater than
0.1.1. In other words, there is nothing that seems to be incompatible with ``djangocms-attributes-field<0.4.0``, so we can add::

    djangocms-attributes-field<0.4.0

to the application's ``requirements.in`` file (*outside* the section that will be overwritten) and
test it, by rebuilding the application with::

    docker-compose build web

If that completes without an error, you will know that you have successfully identified and
addressed the dependency conflict.


Repeat the process
------------------

Often you will need to repeat the process, as further dependency conflicts will be revealed after
you have solved the first one. Each time you will need to pin the problem package in
``requirements.in`` and test the build with ``docker-compose build web``, until you have no
further conflicts.


How to prevent this from happening again
----------------------------------------

In general, the answer is to pin packages firmly, in each place that requirements are given.

An application's requirements can be specified:

* by the addons system in the Control Panel
* in its ``requirements.in`` (addons are automatically listed here too)
* as dependencies of any addons, in their ``setup.py`` files
* as any dependencies of dependencies

You have more control over some of these than others. The easiest way to do this is to pin
requirements manually as necessary in ``requirements.in``. However, if you want more thorough and
precise control, please see :ref:`manage-dependencies`.
