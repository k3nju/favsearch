#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os;
import sys;
import argparse;
import contextlib;

import config;
import db;

def search_by_user_name( db, args ):
	return db.search_by_user_name( args.words, args.user_name );

def search( db, args ):
	return db.search( args.words );

def listup( db, args ):
	return db.listup();

def listup_by_user_name( db, args ):
	return db.listup_by_user_name( args.user_name );

def main( args ):
	handler = listup;
	
	if len( args.words ) == 0 and args.user_name != None:
		handler = listup_by_user_name;
	elif len( args.words ) > 0 and args.user_name != None:
		handler = search_by_user_name;
	elif len( args.words ) > 0 and args.user_name == None:
		handler = search;

	with contextlib.closing( db.Database() ) as fav_db:
		for result in handler( fav_db, args ):
			print( "{0.user_name}:{0.content}".format( result ) );

if __name__ == "__main__":
	parser = argparse.ArgumentParser( description = "Search favorite tweets from database" );
	parser.add_argument(
		"--words", nargs = "+", default = [],
		help = "Specify search words"
	);
	parser.add_argument(
		"--user_name", dest = "user_name", 
		help = "Specify tweet user_name for search"
		);
	
	args = parser.parse_args();
	main( args );
	
