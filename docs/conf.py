# Configuration file for the Sphinx documentation builder.
import guzzle_sphinx_theme
from datetime import datetime

now = datetime.now()

project = "Data Waffe CMS"
copyright = "{}, Matchstick Studio".format(now.year)
author = "Matchstick Studio"

version = "{}.{}.{}".format(*now.isocalendar())
# The full version, including alpha/beta/rc tags.
release = "{}.{}.{}".format(*now.isocalendar())
html_title = "Data Waffe CMS Documentation"
html_short_title = "Data Waffe CMS"

# Custom sidebar templates, maps document names to template names.
html_sidebars = {"**": ["logo-text.html", "globaltoc.html", "searchbox.html"]}

exclude_patterns = ["_build"]

html_static_path = ["_static"]

# -- General configuration

extensions = []

templates_path = ["_templates"]

# -- Options for HTML output

html_theme_path = guzzle_sphinx_theme.html_theme_path()
html_theme = "guzzle_sphinx_theme"
# Guzzle theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the sidebar
    "project_nav_name": "Data Waffe CMS",
}


extensions.append("guzzle_sphinx_theme")

# -- Options for EPUB output
epub_show_urls = "footnote"
