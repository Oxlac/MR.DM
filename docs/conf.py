# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath("."))))

autoapi_dirs = ["../src"]


project = "Mr.DM"
copyright = "2024, Oxlac LLP"
author = "Oxlac LLP"
extensions = ["autoapi.extension", "sphinx_autodoc_typehints"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
root_doc = "docs"
show_authors = True
html_logo = "images/logo.png"
html_favicon = "images/icon.ico"
