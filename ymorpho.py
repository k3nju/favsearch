#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""Client for Yahoo Web API morphology analysis service

You need your "Yahoo Application ID"(AppID) by registering Yahoo developer network
and set your AppID to config.py.
"""


import requests;
import bs4;

import config;

"""Morphology analysis WebAPI URL."""
URL = "http://jlp.yahooapis.jp/MAService/V1/parse"

def request( sentence ):
	"""Returns list of noun phrases by using Yahoo WebAPI.
	"""
	req = {
		"appid"     : config.YAHOO_APP_ID,
		"sentence"  : sentence,
		"results"   : "ma",
		"ma_filter" : "9",
		};
	
	r = requests.post( URL, data = req );
	if r.status_code != 200:
		raise Exception( "Morphology analysis failed" );

	return __parse( r.text );
	
def __parse( xml_data ):
	soup = bs4.BeautifulSoup( xml_data );
	return [ i.text for i in soup.find_all( "surface" ) ];
	
if __name__ == "__main__":
	from pprint import pprint;
	pprint( request( "吾輩は猫である。名前はまだ無い" ) );

