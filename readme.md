# Divio Cloud documentation for developers

Published version: [Divio Cloud developer handbook](http://docs.divio.com/en/latest/).

This documentation is intended for developers using the Divio Cloud.

## Build the documentation locally

You'll need the [enchant](https://www.abisource.com/projects/enchant/) library,
used by ``pyenchant`` for spelling.

Install with ``brew install enchant`` (macOS) or the appropriate command for
your system.

Then:

    git clone git@github.com:divio/divio-cloud-docs.git  # clone
    cd divio-cloud-docs
    make install  # create a virtualenv and install required components
    make run  # build and serve the documentation
    open http://localhost:8001  # open it in a browser


## Notable techniques used in this documentation

### Read the Docs

We serve our documentation via [Read the Docs](https://readthedocs.org), a superb free service that's
especially well-known in the Python world, and is ideal for open-source projects.

The documentation is written in ReStructed Text (RST) and built using [Sphinx](http://sphinx.pocoo.org).

Read the Docs also offers a commercial service via [readthedocs.com](https://readthedocs.com).


### Ad-hoc CSS/JS in pages

We do this on a few pages, where we need something extra.

It's as simple as:

    .. raw:: html

        <style>
            p {color: red;}
        </style>

at the top of the page to add some styles. See the [raw version of the main index.html page for an example](https://raw.githubusercontent.com/divio/divio-cloud-docs/master/index.rst).

We use this to...


### Create responsive columns

See [docs.divio.com](http://docs.divio.com). There, we add the styles you see in the example above, and apply
appropriate classes to the elements:

     .. rst-class:: clearfix row

     .. rst-class:: column column2


     :ref:`Tutorial <introduction>`
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

     Get started with a hands-on introduction to the Divio Cloud for
     developers.

     .. rst-class:: column column2


     :ref:`How-to guides <how-to>`
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

     Step-by-step guides for the developer covering key operations and procedures


     [...]

     .. rst-class:: clearfix row

     About the Divio Cloud
     ---------------------


### Create an interactive debugging checklist

When a deployment fails on our Cloud, our Control Panel will direct you to the [interactive debugging checklist](http://docs.divio.com/en/latest/how-to/debug-deployment-problems.html#debugging-checklist).

It's a kind of [Choose your own adventure story](https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure), but probably
less fun.

This checklist relies on [styles and JavaScript](https://raw.githubusercontent.com/divio/divio-cloud-docs/master/how-to/debug-deployment-problems.rst).


### Sphinx and intersphinx extensions

If you don't already use [intersphinx](http://www.sphinx-doc.org/en/stable/ext/intersphinx.html), you should.

This allows us to link directly to (for example) references in other Sphinx projects, such as [where we link to django CMS's caching settings](http://docs.divio.com/en/latest/reference/caching.html#caching-in-django-cms).

The trick here is that unlike `:ref:` for example, `setting:` is not a natively understood by Sphinx - meaning that
there isn't *by default* a way to refer to those in another project. However, we can *extend* Sphinx's capacities.

See our [extensions.py](https://github.com/divio/divio-cloud-docs/blob/master/extensions.py) for how we do this (we
simply steal the [extensions.py from django CMS](https://github.com/divio/django-cms/blob/develop/docs/_ext/djangocms.py)).

A reference then looks like:

    :setting:`django-cms:CMS_CACHE_DURATIONS`


## Documentation structure

Our documentation structure is key to its usability. See our [What nobody tells you about documentation](https://www.divio.com/en/blog/documentation/) for an
explanation of why it's important and how it works.
