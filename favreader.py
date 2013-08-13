#! /usr/bin/env python
# -*- coding:utf-8 -*-

import twitter;

import common;
import ymorpho;
import config;

"""Read favorite tweets from twitter.
"""
class FavReader():
	def __init__( self ):
		oauth_token, oauth_token_secret = twitter.read_token_file( config.TWITTER_OAUTH_FILE );
		oauth = twitter.OAuth(
			oauth_token,
			oauth_token_secret,
			config.TWITTER_CONSUMER_KEY,
			config.TWITTER_CONSUMER_SECRET
			);
		self.__tw = twitter.Twitter(
			auth = oauth,
			secure = True,
			domain = "api.twitter.com"
			);

	def read( self, page_no, count ):
		tweets = self.__tw.favorites.list( page = page_no, count = count );
		for tweet in tweets:
			# extract TweetEntity members from json response
			user_id	  = tweet[ "user" ][ "id" ]          # user_id
			user_name = tweet[ "user" ][ "screen_name" ] # user_name
			tweet_id  = tweet[ "id" ]                    # tweet_id
			content	  = tweet[ "text" ]                  # content
			# urls
			urls      = set(
				[ i[ "url" ] for i in tweet[ "entities" ][ "urls" ] ]
			);

			# words
			# to get words I need to call Yahoo Web API for morphological analysis
			words = self.__get_words( content, urls );
			
			yield common.TweetEntity(
				user_id,
				user_name,
				tweet_id,
				content,
				words,
				urls
				);

	@staticmethod
	def __get_words( content, urls ):
		for url in urls:
			content = content.replace( url, "" );
		return set( ymorpho.request( content ) );
		
			
if __name__ == "__main__":
	r = FavReader();
	for i in r.read( 20, 1 ):
		from pprint import pprint;
		pprint( i );
