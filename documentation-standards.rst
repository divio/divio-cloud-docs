:orphan:

Documentation standards
=======================

Our documentation structure is key to its usability. See `The documentation system <https://documentation.divio.com>`_
for an explanation of why it's important and how it works.


Column widths
-------------

Wrap new ReStructured Text source to 120 columns.


Headings
--------

Sub-headings
~~~~~~~~~~~~

Sub-sub-headings
^^^^^^^^^^^^^^^^

Sub-sub-sub-headings
....................


Intersphinx
-----------

This documentation knows how to link to documentation in:

* Python
* Django
* django CMS

using Intersphinx.

Examples:

* :ref:`Link to a reference <python:comparisons>`
* :mod:`Link to a module <python:datetime>`
* :doc:`Link to a document <django:topics/email>`
* :class:`Link to a class <django-cms:cms.models.Page>`


Noting references
-----------------

External resources link to this documentation. Any link to a documentation reference must be noted with information
about the external resource, e.g.::

  ..  Do not change this reference! [or document name]
      Referred to by: tutorial message 51 project-create-base-project
      Where: in the project creation dialog e.g. https://control.divio.com/control/project/create/#step-1
      As: https://docs.divio.com/en/latest/background/project-creation-options#project-creation-platform

  .. _project-creation-platform:

External links to documentation references should use the reference (as above) rather than the heading to which it is
attached (in this case https://docs.divio.com/en/latest/background/project-creation-options#platform). This allows
changing headings without the risk of breaking links.


Style guide
------------

Inline formatting
~~~~~~~~~~~~~~~~~~

* italics

  * for emphasis: *Be warned*
  * names of books: *Test-driven development*
  * in interfaces, when referring by name: in the *Settings* menu, select *Add…*

* bold:

  * strong emphasis: **Never** do this!
  * in interfaces, when referring to buttons that perform actions: Select **Save**

* literals:

  * names of things in code: the ``ModelAdmin`` class
  * things you want the user to type: ``cd`` into the new directory

* inverted commas:

  * when quoting text: Call it “My first weblog”
  * for names of chapters in books
  * when there isn’t any better way to refer to something: use the “eye” icon

* examples of what **not** to do with inverted commas:

  * put a link, italics, bold or literals in inverted commas: “`example <#>`_”, the “**Save**” button, select “*Add…*”

Spelling
~~~~~~~~

The documentation uses British English spelling (*-ise* rather than *-ize*, *colour* rather than *color*, etc).

Tone and language
~~~~~~~~~~~~~~~~~

Avoid language that tells the user that something is easy: "just do ...", "simply ...".

In general, use the second person ("This document assumes you are a reasonably experienced software developer") when
referring to the reader (not "The reader is assumed to be...").

Tutorials and how-to guides should adopt the imperative form wherever possible ("Run xxx", "delete yyy").


Ad-hoc CSS/JS in pages
----------------------

We do this on a few pages, where we need something extra.

It's as simple as::

    .. raw:: html

        <style>
            p {color: red;}
        </style>

at the top of the page to add some styles. See the 
`raw version of the main index.html page for an example <https://raw.githubusercontent.com/divio/divio-cloud-docs/master/index.rst>`_.


Create responsive columns
-------------------------

See `docs.divio.com <http://docs.divio.com>`_. There, we add the styles you see 
in the example above, and apply appropriate classes to the elements::

     ..  rst-class:: clearfix row

     ..  rst-class:: column column2


     :ref:`Tutorial <introduction>`
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

     Get started with a hands-on introduction to Divio for developers.

     ..  rst-class:: column column2


     :ref:`How-to guides <how-to>`
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

     Step-by-step guides for the developer covering key operations and procedures


     [...]

     ..  rst-class:: clearfix row

     About Divio
     ------------


Create an interactive debugging checklist
-----------------------------------------

When a deployment fails on our Cloud, our Control Panel will direct you to the 
`interactive debugging checklist <http://docs.divio.com/en/latest/how-to/debug-deployment-problems.html#debugging-checklist>`_.

It's a kind of `Choose your own adventure story <https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure>`_, but probably
less fun.

This checklist relies on specific `styles and JavaScript <https://raw.githubusercontent.com/divio/divio-cloud-docs/master/how-to/debug-deployment-problems.rst>`_.


Sphinx and intersphinx extensions
---------------------------------

This allows us to link directly to (for example) references in other Sphinx 
projects, such as `where we link to django CMS's caching settings <http://docs.
divio.com/en/latest/reference/caching.html#caching-in-django-cms>`_.

The trick here is that unlike `:ref:` for example, `setting:` is not a natively 
understood by Sphinx - meaning that there isn't *by default* a way to refer to 
those in another project. However, we can *extend* Sphinx's capacities.

See our `extensions.py <https://github.com/divio/divio-cloud-docs/blob/master
/extensions.py>`_ for how we do this.

A reference then looks like:

    :setting:`django-cms:CMS_CACHE_DURATIONS`
