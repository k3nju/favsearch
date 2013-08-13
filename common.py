#! /usr/bin/env python
# -*- coding:utf-8 -*-

from collections import namedtuple;

# This tuple represent each of tweets
TweetEntity = namedtuple(
	"TweetEntity",
	[
		"user_id", 
		"user_name",
		"tweet_id",
		"content",
		"words", # words extracted from tweet for full text search
		"urls",  # urls extracted from tweet
	]
);

# This tuple represents search result of tweets
SearchResultEntity = namedtuple(
	"SearchResultEntity",
	[
		"user_name",
		"content",
	]
);
