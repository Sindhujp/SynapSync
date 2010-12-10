import logging
import string

import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from util.sessions import Session
from dbinterface import DataStoreInterface
from stringFormatter import StringFormatter
from emailProcessor import EmailProcessor
import render
 
class EmailHandler(webapp.RequestHandler):
	def get(self):	
		emailObj = EmailProcessor()
		datastore = DataStoreInterface()
				
		emails =  [];
		emails = datastore.getEmailSubscriber('filipmares')
		
		output = ''
		
		for e in emails:
			output += e + '<br>'
		
		self.response.out.write(output)