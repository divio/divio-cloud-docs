Divio Documentation
===================

.. image:: https://readthedocs.com/projects/divio-divio-cloud-docs/badge/?version=latest
    :target: https://docs.divio.com/en/latest/?badge=latest
    :alt: Documentation status

.. image:: https://github.com/divio/divio-cloud-docs/actions/workflows/default.yml/badge.svg
    :target: https://github.com/divio/divio-cloud-docs/actions/workflows/default.yml
    :alt: GitHub workflow status


The official documentation for Divio and its products.


Build the documentation locally
-------------------------------

You'll need the `enchant <https://www.abisource.com/projects/enchant/>`_
library, used by ``pyenchant`` for spelling.

Install with ``brew install enchant`` (macOS) or the appropriate command for
your system.

Then::

    git clone git@github.com:divio/divio-cloud-docs.git
    cd divio-cloud-docs
    make install
    make run
    open http://localhost:9001


Notable techniques used in this documentation
---------------------------------------------

* We serve our documentation via `Read the Docs <https://readthedocs.org>`_.
* The documentation is written in ReStructed Text (RST) and built using 
  `Sphinx <http://sphinx.pocoo.org>`_.
* `Intersphinx <http://www.sphinx-doc.org/en/stable/ext/intersphinx.html>`_
  to reference to other documentation.


Documentation structure and standards
-------------------------------------

Our documentation structure is key to its usability. See our 
`What nobody tells you about documentation <https://documentation.divio.com>`_ 
system for an explanation of why it's important and how it works.

See also our `additional documentation standards 
<https://docs.divio.com/documentation-standards>`_.
