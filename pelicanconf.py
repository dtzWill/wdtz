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

# Tag cloud settings
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100
TAG_CLOUD_SORTING = 'alphabetically'

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
    ('Email', 'mailto:w@wdtz.org', 'fas fa-envelope'),
    ('Mastodon', 'https://mastodon.social/@wdtz', 'fab fa-mastodon'),
    ('Twitter', 'https://twitter.com/wdtz', 'fab fa-twitter'),
    ('Github', 'https://github.com/dtzWill', 'fab fa-github'),
    ('#allvm on OFTC', 'https://riot.im/app/#/room/#_oftc_#allvm:matrix.org', 'fas fa-comment'),)

ACADEMIC = (
    ('Google Scholar', 'https://scholar.google.com/citations?user=DIww2AMAAAAJ&hl=en', 'ai ai-google-scholar'),
    ('ResearchGate', 'https://www.researchgate.net/profile/Will_Dietz', 'ai ai-researchgate'),
    ('ORCID', 'https://orcid.org/0000-0001-7004-2343', 'ai ai-orcid'),)

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
TYPOGRIFY = True

TWITTER_USERNAME = "wdtz"

SUMMARY_END_MARKER = "PELICAN_END_SUMMARY"

LOAD_CONTENT_CACHE = False
CACHE_CONTENT = False
DELETE_OUTPUT_DIRECTORY = True

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["plugin_pipeline", "neighbors", "optimize_images", "tag_cloud"]

PLUGIN_PIPELINE = [ "wrap_figures", "replace_tt", "summary", "remove_summary_footnotes", "nbsp_footnotes", "unify_footnotes" ]

# Favicon support
STATIC_PATHS = [
    'extra/favicon.ico',
    'images',
    'academicons'
]

EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'images': {'path': 'images'},
    'academicons': {'path': 'academicons'}
}
