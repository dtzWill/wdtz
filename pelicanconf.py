#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Will Dietz'
SITENAME = "wdtz / Will Dietz"
SITE_TAGLINE = "Where There's a Will There's a Way"

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
FEED_ATOM = None
FEED_RSS = None

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('Twitter', 'http://twitter.com/wdtz'),
    ('Github', 'http://github.com/dtzWill'),
    ('Facebook', 'http://facebook.com/dtzWill'),
    ('Google-Plus', 'http://wdtz.org/+'),
    ('##uiuc on Freenode', 'http://webchat.freenode.net/?channels=%23%23uiuc'),)

DEFAULT_PAGINATION = 5
DEFAULT_ORPHANS = 0

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

USE_FOLDER_AS_CATEGORY = True
DISPLAY_PAGES_ON_MENU = True

THEME = "bootstraped"

DEFAULT_TRUNCATE = 500
NON_GENERIC_BOOTSTRAP = "cyborg"
EMAIL_ADDRESS = "wdietz2@uiuc.edu"

# Typographic improvements
# TYPOGRIFY = True

TWITTER_USERNAME = "wdtz"

SUMMARY_END_MARKER = "PELICAN_END_SUMMARY"

PLUGIN_PATH = "/home/will/pelican-plugins"
PLUGINS = ["neighbors", "summary", "optimize_images"]
