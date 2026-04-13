# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Safe Grading Framework'
copyright = '2026, Kacie Beckett - University of Melbourne'
author = 'Kacie Beckett'
release = 'V0.5.0'

import sys
from pathlib import Path

sys.path.insert(0, str(Path('../..', '').resolve()))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx_autodoc_typehints',
]


# Autodoc settings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'special-members': '__init__',
    'private-members': False,
    'inherited-members': False,
}

templates_path = ['_templates']
exclude_patterns = []

# GitHub Pages configuration
html_baseurl = 'https://comp10001.github.io/py-safe-grading-framework/'
html_context = {
    'display_github': True,
    'github_user': 'COMP10001',
    'github_repo': 'py-safe-grading-framework',
    'github_version': 'main',
    'conf_py_path': '/docs/source/',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'canonical_url': html_baseurl,
}

html_title = f"{project} v{release} Documentation"
html_short_title = f"{project} v{release}"

