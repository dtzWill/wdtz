#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Will Dietz'
SITENAME = "wdtz / Will Dietz"
SITE_TAGLINE = "Where There's a Will There's a Way"

TIMEZONE = 'America/Chicago'

DEFAULT_DATE_FORMAT = '%a %m/%d/%y'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
FEED_ATOM = None
FEED_RSS = None

THEME_CHANGER = True

DEV_THEMES = [
    'Cerulean',
    'Cosmo',
    'Cyborg',
    'Darkly',
    'Flatly',
    'Journal',
    'Lumen',
    'Readable',
    'Simplex',
    'Slate',
    'Spacelab',
    'Superhero',
    'United',
    'Yeti',
]

# Blogroll
# LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('Email', 'mailto:wdietz2@uiuc.edu', 'fa-envelope'),
    ('Twitter', 'http://twitter.com/wdtz', 'fa-twitter'),
    ('Github', 'http://github.com/dtzWill', 'fa-github'),
    ('Facebook', 'http://facebook.com/dtzWill', 'fa-facebook-square'),
    ('Google-Plus', 'http://wdtz.org/+', 'fa-google-plus'),
    ('##uiuc on Freenode', 'http://webchat.freenode.net/?channels=%23%23uiuc', 'fa-comment'),)

DEFAULT_PAGINATION = 5
DEFAULT_ORPHANS = 0

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

USE_FOLDER_AS_CATEGORY = True
DISPLAY_PAGES_ON_MENU = True

THEME = "bootstraped"

DEFAULT_TRUNCATE = 500
NON_GENERIC_BOOTSTRAP = "cyborg"

# Typographic improvements
# Disable since it attemps to insert CAPS span in title!
# TYPOGRIFY = True

TWITTER_USERNAME = "wdtz"

SUMMARY_END_MARKER = "PELICAN_END_SUMMARY"

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["neighbors", "wrap_figures", "summary", "optimize_images"]


# Favicon support
STATIC_PATHS = [
    'extra/favicon.ico',
    'images',
]

EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'images': {'path': 'images'},
}
