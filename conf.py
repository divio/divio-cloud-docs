# Configuration file for the Sphinx documentation builder.
#
# Full list of options can be found in the Sphinx documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

#
# -- sys.path preparation ----------------------------------------------------
#

import os
import sys
import datetime
sys.path.insert(0, os.path.abspath("."))


#
# -- Project information ------------------------------------------------------
#

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

project = "Divio Documentation"
full_title = project
copyright = f"{datetime.date.today().year} Divio Technologies AB"
author = "Divio"
version = "2.0"
release = version

#
# -- General configuration ----------------------------------------------------
#

extensions = [
    "extensions",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinxcontrib.mermaid",
    "sphinx_inline_tabs",
    "sphinx_click",
    "notfound.extension",
    "sphinx_reredirects",
]

if "spelling" in sys.argv:
    extensions.append("sphinxcontrib.spelling")

mermaid_version="8.11.4"

#
# -- Options for intersphinx --------------------------------------------------
#

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": (
        "https://docs.djangoproject.com/en/2.2/",
        "https://docs.djangoproject.com/en/2.2/_objects/"
    ),
    "django-cms": ("https://docs.django-cms.org/en/latest/", None),
    "celery": ("https://docs.celeryproject.org/en/stable/", None),
    "whitenoise": ("https://whitenoise.evans.io/en/stable/", None),
    "flask": ("https://flask.palletsprojects.com/", None),
}

#
# -- Options for the theme ----------------------------------------------------
#

html_theme = "furo"
html_theme_options = {
    "show_cloud_banner": False,
    "segment_id": "FT34iqltJg6YdIX5fcyIt5J035FmSAAq",
    "style_external_links": True,
    "navigation_depth": 2,
    "sidebar_hide_name": True,
}

#
# -- Options for HTML output --------------------------------------------------
#

html_title = full_title
html_help_basename = "DivioDocumentation"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
    "styles/furo.css",
]

#
# -- Options for Sphinx -------------------------------------------------------
#

source_suffix = ".rst"
master_doc = "index"
language = None
exclude_patterns = ["README.rst", "_build", "Thumbs.db", ".DS_Store", "env", "**/includes"]
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

#
# -- Options for spelling -----------------------------------------------------
#

spelling_lang = "en_GB"
spelling_word_list_filename = "spelling_wordlist"
spelling_ignore_pypi_package_names = True

#
# -- Options for latex output -------------------------------------------------
#

latex_documents = [
    (master_doc, html_help_basename + ".tex", full_title, author, "manual"),
]

#
# -- Options for manual page output -------------------------------------------
#

man_pages = [
    (master_doc, html_help_basename, full_title, [author], 1)
]

#
# -- Options for TODOs --------------------------------------------------------
#

todo_include_todos = True
todo_link_only = True
todo_emit_warnings = False

#
# -- Redirects for broken links -----------------------------------------------
#

# The following represents a valid redirect pattern example for renaming/deleting a file
# inside the how-to folder called configure-settings.rst to django-configure-settings.rst
# that must be included inside redirects dictionary below.

# Redirect pattern:
# "how-to/configure-settings/index.html": "../django-configure-settings",

redirects = {
     "how-to/configure-settings/index.html": "../django-configure-settings",
}