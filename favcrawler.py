#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os;
import sys;
import contextlib;
import argparse;
import traceback;

import favreader;
import db;
import ymorpho;
import config;

def print_error( *msgs ):
	print( "[!] " + " ".join( [ str( i ) for i in msgs ] ), file = sys.stderr );

def main( page_no, count ):
	reader = favreader.FavReader();
	with contextlib.closing( db.Database() ) as fav_db:
		for page_no in range( 1, page_no + 1 ):
			inserted_count = 0;
			for tweet_ent in reader.read( page_no, count ):
				try:
					if fav_db.has_inserted( tweet_ent ):
						continue;
					fav_db.insert( tweet_ent );
					inserted_count += 1;
				except Exception as E:
					traceback.print_exc();
					print_error(
						"Error: insert failed\n",
						"page no:", page_no, "count:", count, "\n",
						E );
					break;
			
			if inserted_count == 0:
				break;

if __name__ == "__main__":
	parser = argparse.ArgumentParser( description = "Crawle favorite tweets and save to database." );
	parser.add_argument(
		"--page_no", dest = "page_no", default = 2000,
		help = "Maximum page number for crawling."
		);
	parser.add_argument(
		"--count", dest = "count", default = 200,
		help = "Tweet count for each read request."
		);
	parser.add_argument(
		"--init", dest = "init", action = "store_true", default = False,
		help = "Create database file."
		);

	args = parser.parse_args();
	
	if args.init == True:
		if os.path.exists( config.DB_FILE ) == True:
			print_error( "Database file already exists: ", config.DB_FILE );
			sys.exit( -1 );
		with contextlib.closing( db.Database() ) as fav_db:
			fav_db.create_tables();
		sys.exit();
	
	main( args.page_no, args.count );
