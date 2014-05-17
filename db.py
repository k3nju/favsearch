#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys;
import sqlite3;
import contextlib;

import common;
import sql;
import config;


"""SQLite3 database wrapper class.

This class wraps SQL operations for SQLite3.
Actual SQL statements are at sql.py.
"""
class Database():
	def __init__( self ):
		self.__conn = sqlite3.connect(
			config.DB_FILE,
			isolation_level = "EXCLUSIVE"
		);
		self.__conn.execute( "pragma foreign_key = on;" );
		
	def close( self ):
		"""Close database connection"""

		if self.__conn != None:
			self.__conn.close();
			self.__conn = None;
	
	def create_tables( self ):
		"""Create tables

		create tables in database file.
		if database file and tables already exist, this method will be failed.
		"""

		for name in dir( sql ):
			if name.lower().endswith( "table" ) == False:
				continue;
			
			self.__conn.execute( getattr( sql, name ) );

	def has_inserted( self, tweet ):
		"""Return True if tweet has been inserted, or return False

		tweet is object of common.TweetEntity.
		"""
		
		with contextlib.closing( self.__conn.execute( sql.HAS_INSERTED, ( tweet.tweet_id, ) ) ) as cur:
			if len( cur.fetchall() ) == 1:
				return True;
			else:
				return False;
	
	def insert( self, tweet ):
		"""Insert tweet entity.
		
		tweet is object of common.TweetEntity.
		"""
		
		self.__conn.execute( "BEGIN" );
		try:
			self.__insert_users( tweet.user_id, tweet.user_name );
			self.__insert_tweet( tweet.tweet_id, tweet.user_id, tweet.content, tweet.tweeted_at );
			self.__insert_fts( tweet.tweet_id, tweet.words );
			self.__insert_urls( tweet.tweet_id, tweet.urls );
		except Exception as E:
			self.__conn.rollback();
			raise;
		else:
			self.__conn.commit();

	def __insert_users( self, user_id, user_name ):
		return self.__execute_insert( sql.ADD_USER, ( user_id, user_name, user_id ) );
	
	def __insert_tweet( self, tweet_id, user_id, content, tweeted_at ):
		return self.__execute_insert( sql.ADD_TWEET, ( tweet_id, content, tweeted_at, user_id, tweet_id ) );

	def __insert_fts( self, tweet_id, words ):
		return self.__execute_insert( sql.ADD_FTS, ( " ".join( words ), tweet_id ) );

	def __insert_urls( self, tweet_id, urls ):
		rowcount = 0;
		for url in urls:
			rowcount += self.__execute_insert( sql.ADD_URL, ( url, tweet_id, url ) );
		return rowcount;

	def __execute_insert( self, sql, args ):
		with contextlib.closing( self.__conn.execute( sql, args ) ) as cur:
			return cur.rowcount;

	def search( self, words ):
		"""Search tweets by words

		words is array of word to be searched by using full text search.
		"""
		yield from self.__execute_select(
			sql.SEARCH,
			( " ".join( words ), )
		);
	
	def search_by_user_name( self, words, user_name ):
		"""Search tweets by words from specified user's tweets"""

		yield from self.__execute_select(
			sql.SEARCH_BY_USER_NAME,
			( user_name, " ".join( words ) )
			);
	
	def listup( self ):
		"""List up all tweets"""

		yield from self.__execute_select( sql.LISTUP );

	def listup_by_user_name( self, user_name ):
		"""List up all specified user's tweets"""
		
		yield from self.__execute_select(
			sql.LISTUP_BY_USER_NAME,
			( user_name, )
		);

	def __execute_select( self, sql, args = () ):
		with contextlib.closing( self.__conn.execute( sql, args ) ) as cur:
			for rec in cur.fetchall():
				 yield common.SearchResultEntity(
					 rec[0],
					 rec[1]
				 );
	
if __name__ == "__main__":
	import os;
	config.DB_FILE = "/tmp/test.db";
	if os.path.exists( config.DB_FILE ):
		os.remove( config.DB_FILE );
	
	db = Database();
	db.create_tables();

	import contextlib;
	with contextlib.closing( db ) as db:
		from datetime import datetime;
		now = datetime.now();
		import common;
		db.insert(
			common.TweetEntity(
				1,
				"hoge",
				1,
				"Hello World http://example.com",
				[ "Hello", "World" ],
				[ "http://example.com" ],
				now
			)
		);
		db.insert(
			common.TweetEntity(
				1,
				"hoge",
				2,
				"The quick brown jumps over the lazy dog http://example.com http://example.com http://example2.com",
				"The quick brown jumps over the lazy dog".split(),
				"http://example.com http://example.com http://example2.com".split(),
				now
			)
		);
		db.insert(
			common.TweetEntity(
				2,
				"hige",
				3,
				"stay hungry, stay foolish",
				"stay hungry stay foolish".split(),
				[],
				now
			)
		);
		db.insert(
			common.TweetEntity(
				2,
				"hige",
				4,
				"quick and lazy",
				"quick and lazy".split(),
				[],
				now
			)
		);
		
		for result in db.search( [ "quick", ] ):
			print( result );
		print( "------------" );
		for result in db.search_by_user_name( [ "quick", ], "hige" ):
			print( result );
		
