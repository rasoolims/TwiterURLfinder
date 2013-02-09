#! /usr/bin/python
# coding=utf8
 

__author__="Mohammad Sadegh Rasooli <rasooli@cs.columbia.edu>"
__date__ ="Feb, 2013"

import sys
import codecs
import re
from collections import defaultdict
from twython import Twython

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


class urlfinder:
	urlList=dict()
	urlMatcher = re.compile('^(http|https|ftp)\://([a-zA-Z0-9\.\-]+(\:[a-zA-Z0-9\.&amp;%\$\-]+)*@)*((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|localhost|([a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(\:[0-9]+)*(/($|[a-zA-Z0-9\.\,\?\'\\\+&amp;%\$#\=~_\-]+))*$')


	'''
		Constructor
	'''
	def __init__(self):
		self.urlList=dict()
		app_key = 'q4tMdAgUQ3XA9EiLBaV4A'
		app_secret = 'jbbSDdndqvWnVFLFgXEQ9zRexE4aY2gFuk6Ih2A1kU'
		access_token = '1143718910-DO89DWRuJPMTxl5qm1uCsd5RDUnUC1J5HH58FIH'
		access_token_secret = 'qRxIbLIv0BeXOHeep5wcorJpgXRGthPd7wrNTCvO6k'
		self.tweet=Twython(app_key=app_key, app_secret=app_secret, oauth_token=access_token,oauth_token_secret=access_token_secret)

	'''
		Checks whether a string is a url or not
	'''
	def isUrl(self,urlCand):
		#print urlCand
		if type(urlCand)!=unicode and type(urlCand)!=str:
			return False

		if self.urlMatcher.match(urlCand):
			return True
		return False


	'''
		Iteratively find urls in the result data structure
	'''
	def getUrls(self,result):
		if type(result)==dict:
			for res in result:
				value=result[res]
				if type(value)==dict or type(value)==list:
					self.getUrls(value)
				elif self.isUrl(value):
					if self.urlList.has_key(value):
						self.urlList[value]+=1
					else:
						self.urlList[value]=1
		else:
			for value in result:
				if type(value)==dict or type(value)==list:
					self.getUrls(value)
				elif self.isUrl(value):
					if self.urlList.has_key(value):
						self.urlList[value]+=1
					else:
						self.urlList[value]=1


	'''
		The main method to call for finding all the distinct urls
	'''
	def findUrls(self,hashtag,maxRes):
		self.urlList=dict()
		search = self.tweet.search(q=hashtag,  count=maxRes)
		for s in search:
			self.getUrls(search)


if len(sys.argv)<2 or sys.argv[1]=='--help':
	print 'A program to find unique urls in 100 recent tweets for a specified hashtag'
	print 'USAGE: python find_twit_url.py [hashtag]'
	print 'In order to find #ibm:  python find_twit_url.py  ibm --or-- python find_twit_url.py  \'#ibm\''
	print 'Copyright: Mohammad Sadegh Rasooli (rasooli@cs.columbia.edu)'
else:
	try:
		finder=urlfinder()
		hashtag=sys.argv[1].decode('utf-8')
		finder.findUrls(hashtag,100)
		for url in finder.urlList.keys():
			print url
	except:
		sys.stderr.write('Error! Please check you connection or input string\n')



	
