#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys;
import sqlite3;

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
		if self.__conn != None:
			self.__conn.close();
			self.__conn = None;
	
	def create_tables( self ):
		for name in dir( sql ):
			if name.lower().endswith( "table" ) == False:
				continue;
			
			self.__conn.execute( getattr( sql, name ) );

	def insert( self, tweet ):
		"""Insert tweet entity.
		
		tweet is object of common.TweetEntity.
		"""
		self.__conn.execute( "BEGIN" );
		try:
			self.__insert_users( tweet.user_id, tweet.user_name );
			self.__insert_tweet( tweet.tweet_id, tweet.user_id, tweet.content );
			self.__insert_fts( tweet.tweet_id, tweet.words );
			self.__insert_urls( tweet.tweet_id, tweet.urls );
		except Exception as E:
			self.__conn.rollback();
			raise;
		else:
			self.__conn.commit();

	def __insert_users( self, user_id, user_name ):
		self.__conn.execute( sql.ADD_USER, ( user_id, user_name, user_id ) );

	def __insert_tweet( self, tweet_id, user_id, content ):
		self.__conn.execute( sql.ADD_TWEET, ( tweet_id, content, user_id, tweet_id ) );

	def __insert_fts( self, tweet_id, words ):
		self.__conn.execute( sql.ADD_FTS, ( " ".join( words ), tweet_id ) );

	def __insert_urls( self, tweet_id, urls ):
		for url in urls:
			self.__conn.execute( sql.ADD_URL, ( url, tweet_id, url ) );

	def search( self, words ):
		yield from self.__execute_sql(
			sql.SEARCH,
			( " ".join( words ), )
		);
	
	def search_by_user_name( self, words, user_name ):
		yield from self.__execute_sql(
			sql.SEARCH_BY_USER_NAME,
			( user_name, " ".join( words ) )
			);
	
	def listup( self ):
		yield from self.__execute_sql( sql.LISTUP );

	def listup_by_user_name( self, user_name ):
		yield from self.__execute_sql(
			sql.LISTUP_BY_USER_NAME,
			( user_name, )
		);
	
	def __execute_sql( self, sql, args = () ):
		cur = self.__conn.cursor();
		cur.execute( sql, args );
		for rec in cur.fetchall():
			yield common.SearchResultEntity(
				rec[0],
				rec[1]
				);
		cur.close();

if __name__ == "__main__":
	import os;
	config.DB_FILE = "/tmp/test.db";
	if os.path.exists( config.DB_FILE ):
		os.remove( config.DB_FILE );
	
	db = Database();
	db.create_tables();

	import contextlib;
	with contextlib.closing( db ) as db:
		import common;
		db.insert(
			common.TweetEntity(
				1,
				"hoge",
				1,
				"Hello World http://example.com",
				[ "Hello", "World" ],
				[ "http://example.com" ]
			)
		);
		db.insert(
			common.TweetEntity(
				1,
				"hoge",
				2,
				"The quick brown jumps over the lazy dog http://example.com http://example.com http://example2.com",
				"The quick brown jumps over the lazy dog".split(),
				"http://example.com http://example.com http://example2.com".split()
			)
		);
		db.insert(
			common.TweetEntity(
				2,
				"hige",
				3,
				"stay hungry, stay foolish",
				"stay hungry stay foolish".split(),
				[]
			)
		);
		db.insert(
			common.TweetEntity(
				2,
				"hige",
				4,
				"quick and lazy",
				"quick and lazy".split(),
				[]
			)
		);
		
		for result in db.search( [ "quick", ] ):
			print( result );
		print( "------------" );
		for result in db.search_by_user_name( [ "quick", ], "hige" ):
			print( result );
		
