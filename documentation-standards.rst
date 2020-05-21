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
