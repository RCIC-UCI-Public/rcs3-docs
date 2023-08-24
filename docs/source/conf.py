# Configuration file for the Sphinx documentation builder.

# -- Project information

project = u'RCS3'
copyright = u'2019-2023, The Regents of the University of California'
author = u'RCIC'

release = '1.0'
version = '1.0.0'

# add path to python code snippets
import sys
import os
sys.path.insert(0, os.path.abspath('src'))

# -- General configuration
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output
html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = '.rst'
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# custom dir for storing pdf files
html_static_path = [ '_static', 'pdfs']

# top sidebar image image (relative to this dir)
html_logo = 'images/rcic-logo.png'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%Y-%m-%d'

#keep for reference
html_theme_options = {
    # use this to show only logo on top of the side bar without
    # home button link as it is on every page at the top already
    'logo_only': True,
	##### the following are for a reference #####
    # top portion of sidebar background
    #'style_nav_header_background': '#353130',
    #'display_version': True,
    #'prev_next_buttons_location': 'both',
    #'style_external_links': False,
    # Toc options
    #'collapse_navigation': True,
    #'sticky_navigation': True,
    #'navigation_depth': 4,
    #'includehidden': True,
    #'titles_only': False
}
