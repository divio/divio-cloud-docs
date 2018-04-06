.. _debug-dependency-conflict:

How to identify and resolve a dependency conflict
=================================================


Example error::

    Could not find a version that matches Django<1.10,<1.10.999,<1.11,<1.12,<1.9.999,<2,
    <2.0,==1.9.13,>1.3,>=1.11,>=1.3,>=1.4,>=1.4.10,>=1.4.2,>=1.5,>=1.6,>=1.7,>=1.8

Packages in your project specified conflicting dependencies. In the example above, there is no
version of Django that matches the constraint ``>=1.11`` and also several of the others.

This can happen when you have specified versions of packages that themselves require conflicting
versions of some other package. Often, especially in a project that used to work, it's caused by an
unpinned requirement, that then demands an unexpected dependency.

We can see from the error that ``Django>=1.11`` is the problem, so we can search through the log to
find what added it:

..  code-block:: text

    adding Django>=1.11
      from django-phonenumber-field==2.0.0

A search for ``adding django-phonenumber-field`` reveals:

..  code-block:: python

    adding django-phonenumber-field>=0.7.2
      from aldryn-people==1.2.2

So ``django-phonenumber-field`` isn't pinned adequately in Aldryn People.

The solution is to pin any packages to versions that have compatible dependencies, either in the
project's ``requirements.in``, or (if possible) in the ``setup.py`` of the other packages that
installed them::

    django-phonenumber-field<2.0.0

Locally, the project can be tested for dependency conflicts of this sort by running
``docker-compose build web``.
