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

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('Email', 'http://www.google.com/recaptcha/mailhide/d?k=01sjWttqALQwPoufFVhsbSgg==&c=O5DKj0E0KM4igqH2agQcbtZfhjmI7uQDXGZabETy5rI="', 'icon-envelope'),
    ('Twitter', 'http://twitter.com/wdtz', 'icon-twitter'),
    ('Github', 'http://github.com/dtzWill', 'icon-github'),
    ('Facebook', 'http://facebook.com/dtzWill', 'icon-facebook-sign'),
    ('Google-Plus', 'http://wdtz.org/+', 'icon-google-plus'),
    ('##uiuc on Freenode', 'http://webchat.freenode.net/?channels=%23%23uiuc', 'icon-comment'),)

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
# TYPOGRIFY = True

TWITTER_USERNAME = "wdtz"

SUMMARY_END_MARKER = "PELICAN_END_SUMMARY"

PLUGIN_PATH = "plugins"
PLUGINS = ["neighbors", "wrap_figures", "summary", "optimize_images"]


# Favicon support
STATIC_PATHS = [
    'extra/favicon.ico',
    'images',
]

EXTRA_PATH_METADATA = {
    'extra/favicon.ico' : { 'path' : 'favicon.ico' },
    'images' : { 'path' : 'images' },
}
