#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Harry'
SITENAME = 'scribbles and babbles'
SITEURL = 'https://pseudobabble.github.io'

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

THEME = 'resume-blue'

# pelican-blue params
SOCIAL = (('linkedin', 'https://www.linkedin.com/in/harry-johnson-7044b330/'),
          ('github', 'https://github.com/pseudobabble'),
          #          ('twitter', 'https://twitter.com/username'),
          )

SIDEBAR_DIGEST = 'Software Engineering, mostly'

# FAVICON = 'url-to-favicon'

DISPLAY_PAGES_ON_MENU = True

# TWITTER_USERNAME = 'twitter-user-name'

MENUITEMS = (('Blog', SITEURL),)

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True


# Plugins
PLUGIN_PATHS = ['../plugins']
PLUGINS = ['pelican_javascript']
