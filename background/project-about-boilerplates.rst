.. _about-boilerplates:

Boilerplates
==================

.. _boilerplates_reference:

Boilerplates
------------

A **Boilerplate** is a convenient way to define components to be used by a project, so that new
projects can be created quickly with the same tooling set up as soon as the project is created.

A Boilerplate can be used to define any project-level components and processes that are to be
re-used.

For example, a Boilerplate can define how the Django templates are structured and make opinionated
choices about what JavaScript frameworks and CSS tools are used.

When a project is created, it will always specify a Boilerplate - even if it's a pre-defined
:ref:`blank-boilerplate` that leaves all these choices up to you.

Various Boilerplates are provided as defaults. Some provide only basic HTML and CSS,
whereas more sophisticated ones include advanced frontend tooling: NPM, webpack, Sass and other
components.


.. _built-in-boilerplates:

Our built-in Boilerplates
-------------------------

This list represents some key built-in Boilerplates.


.. _blank-boilerplate:

Blank Boilerplate
~~~~~~~~~~~~~~~~~

The `Blank Boilerplate <https://github.com/aldryn/aldryn-boilerplate-blank>`_
installs no components. It will be up to you to install anything you need,
including templates for your site.


HTML5 Boilerplate
~~~~~~~~~~~~~~~~~

Our `HTML5 Boilerplate <https://github.com/divio/djangocms-boilerplate-html5>`_
implements the `HTML5 Boilerplate package <https://html5boilerplate.com>`_. The
HTML5 Boilerplate package is a popular starter set of starter files, which
includes a generic HTML template, CSS to normalise and set some standard
classes, and some JavaScript including jQuery.

Our implementation of it is very standard, and simply adapts it for use in
django CMS projects.


Bootstrap and Foundation Boilerplates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our `Bootstrap <https://github.com/divio/djangocms-boilerplate-bootstrap3>`_
and `Foundation <https://github.com/divio/djangocms-boilerplate-foundation6>`_
Boilerplates implement these two popular frontend frameworks.

They are both fully-featured frameworks that include opinionated CSS and
JavaScript for your own use, and numerous built-in widgets and standardised web
components.


Sass Boilerplate
~~~~~~~~~~~~~~~~

Our `Sass Boilerplate <https://github.com/divio/djangocms-boilerplate-sass>`_
introduces compiled components. This is a *dynamic Boilerplate*, unlike those
above, which is to say that it compiles its own materials at runtime (the
*static Boilerplates* by contrast simply use or serve the materials they ship
with).

The Sass Boilerplate uses the `HTML5 Boilerplate package
<https://html5boilerplate.com>`_ as its basis. It uses:

* `Gulp <http://gulpjs.com>`_ to run the compilation
* `npm <https://www.npmjs.com>`_ as a package manager
* `Node <https://nodejs.org/en/>`_ as a runtime environment.

The advantage of using a dynamic Boilerplate with compiled components is that
it permits you to build a customised frontend, shorn of items your project does
not require. Compiled components can also be heavily compressed and optimised,
while the source files you work on can remain readable and comprehensive.


Webpack Boilerplate
~~~~~~~~~~~~~~~~~~~

The `Webpack Boilerplate
<https://github.com/divio/djangocms-boilerplate-webpack>`_ implements the
Bootstrap framework as a fully-compiled frontend set-up. It uses:

* `Gulp <http://gulpjs.com>`_ to run the compilation
* `Webpack <https://webpack.js.org>`_ to bundle all the modules
* `npm <https://www.npmjs.com>`_ as a package manager
* `Node <https://nodejs.org/en/>`_ as a runtime environment.
