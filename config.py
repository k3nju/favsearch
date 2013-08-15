#! /usr/bin/env python
# -*- coding:utf-8 -*-

import privates;

"""Configuration file.

NOTICE: Important configuration data are imported from privates.py.
        You need to write own your privates.py.
        See detail in privates.py.example.
"""


"""SQLite3 database file"""
DB_FILE = "/usr/local/tmp/tw.db";

# imported from privates

"""OAUTH file used by twitter module"""
TWITTER_OAUTH_FILE = privates.OAUTH_FILE;
"""Consumer key used by twitter module"""
TWITTER_CONSUMER_KEY = privates.CONSUMER_KEY;
"""Consumer key used by twitter module"""
TWITTER_CONSUMER_SECRET = privates.CONSUMER_SECRET;

"""Yahoo application ID"""
YAHOO_APP_ID = privates.APP_ID;
