#!/usr/bin/env python

import argparse
import urllib
import sys
import json
from os.path import basename
import os
import re

def getOtherMovieTitles(imdb_title,searchString,exclude):

	other_movies =[]
	
	searchParams = {}
	searchParams['q'] = searchString
	searchParams['tt'] = 'on'
	searchParams['json'] = '1'
	searchParams['nr'] = '1'
	apicall = urllib.urlopen('http://www.imdb.com/xml/find?%s' % urllib.urlencode(searchParams))
	result = apicall.read().encode('utf-8')
	apicall.close()

	data = json.loads(result)
	
	#Get popular movies from data
	if 'title_popular' in data:
		popular_movies = data['title_popular']

		for movie in popular_movies:
			other_popular_title = movie['title'].encode('utf-8')
			other_popular_description = movie['title_description'].split(',')
			if exclude==False or other_popular_title != imdb_title:
				oData = other_popular_title + ": "+ other_popular_description[0]
				other_movies.append(oData)
	return other_movies

def fetch(params):

	if len(params) == 0:
		print 'Insufficient arguments. Please check documentation.'
		return

	### call IMDb API
	apicall = urllib.urlopen('http://www.omdbapi.com/?%s' % urllib.urlencode(params))
	result = apicall.read()
	apicall.close()

	# print requested info
	data = json.loads(result)
	
	return data
	
def getMovieName(path):
	file_name = basename(path)
	mov = re.sub(r'[\d+].*$',"",os.path.splitext(file_name)[0])
	year = re.search(r'(\d+)',os.path.splitext(file_name)[0])
	return (re.sub(r'[(.]',' ',mov).rstrip(),year.group())
	
parser = argparse.ArgumentParser(description='Get IMDb data for a movie')

parser.add_argument("-t", help="Movie title")
parser.add_argument("-y", help="Year of release", type=int)
parser.add_argument("-r", help="Return raw XML/JSON response", choices=['JSON','XML'])

args = parser.parse_args()

params = {}
keys = ['t', 'y', 'r']
for k in keys:
	if args.__getattribute__(k): params[k] = args.__getattribute__(k)

params['t'] , params['y'] = getMovieName(args.__getattribute__('t'))

others = []
data = fetch(params)

if data is None:
	parser.print_usage()
elif 'Title' in data:
	title = data['Title']
	others = getOtherMovieTitles(title,params['t'],True)
	
	print '\n'
	print "*************** Listing results for", params['t'].upper()," **********************"
	for k in data:
		print k.upper() + ":",
		print data[k].encode('utf-8')
  
	if len(others)>0:
		print "******************** Other popular movie titles *******************************"
		for movie in others:
			print movie
else:
	print 'Sorry!!! No results to show'


				
 

