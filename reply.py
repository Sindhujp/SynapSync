import logging
import string
import wsgiref.handlers
#from google.appengine.ext.webapp import blobstore_handlers
#from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from util.sessions import Session
from dbinterface import DataStoreInterface
from stringFormatter import StringFormatter
from emailProcessor import EmailProcessor
from util.twitter_oauth_handler import *
import util.twitter_oauth_handler as twitter_oauth_handler
import util.facebook.__init__ as facebook
from time import time
from bitly import *
import render


API_KEY = 'bba630a5c803425bbb00cb137fe0894c'
SECRET_KEY = 'e55f6309bedf9a34a6334a5ccabf7bfe' 

class TwitterReplyHandler(webapp.RequestHandler):

	def get(self):
		self.session = Session()	
		if 'user' in self.session:
			user = self.session['user']
			params = (self.request.url).split('?')[1].split('&')
			render.doRender(self, 'reply.html', {'user': user, 'name': '@' + params[2].split('=')[1]})
		else:
			self.redirect('main.html')
	
	def post(self):
		#intialization of variables
		self.session = Session()
		if 'user' in self.session:
			user = self.session['user']		
			error=''
			
			formatter = StringFormatter()
			company = formatter.getCompany(user)
			profileName = formatter.getCompanyProfileName(user)
			
			#retrieving content from form fields		
			title = self.request.get('txtTitle')
			id = formatter.formatID(title)
			content = self.request.get('txtContent')
			btnClicked = formatter.getButtonType(self.request.body)
				
			if title<>'':

				response = ''
				if (btnClicked == 'Post'):
				
					params = (self.request.url).split('?')[1].split('&')
					twitterAccounts = datastore.getTwitterAccounts(profileName)
					twitter = twitterAccounts
					for name in twitter:
						if name == params[1].split('=')[1]:
							client = OAuthClient('twitter', self, name)
							response = client.post('/statuses/update', status = title, in_reply_to_status_id = params[0].split('=')[1])
				
				if response == "SynapSync could not post to Twitter. The server could not be contacted at this time. Please try again later.":
					self.response.out.write(response)
					return
				
			else:
				error = 'Please fill the Title and Content fields below!' 
			self.redirect('controlpanel.html')

			
class FacebookReplyHandler(webapp.RequestHandler):

	def get(self):
	
		self.session = Session()	
		if 'user' in self.session:
			user = self.session['user']
			render.doRender(self, 'reply.html', {'user': user})
		else:
			self.redirect('main.html')
			
	def post(self):
		#intialization of variables
		self.session = Session()
		if 'user' in self.session:
			user = self.session['user']		
			error=''
			
			formatter = StringFormatter()
			company = formatter.getCompany(user)
			profileName = formatter.getCompanyProfileName(user)
			
			#retrieving content from form fields		
			title = self.request.get('txtTitle')
			id = formatter.formatID(title)
			content = self.request.get('txtContent')
			btnClicked = formatter.getButtonType(self.request.body)
				
			if title<>'':

				response = ''
				if (btnClicked == 'Post'):
				
					params = (self.request.url).split('?')[1].split('&')
					facebookAccounts = datastore.getFacebookAccounts(profileName)
					for fb in facebookAccounts:
						if fb.dbUid == params[1].split('=')[1]:
							fb = facebook.Facebook(API_KEY, SECRET_KEY)
							response = fb.__call__('Stream.addComment', {'post_id':params[0].split('=')[1], 'comment':title, 'uid':params[1].split('=')[1]})
				
				if response == "SynapSync could not post to Facebook. The server could not be contacted at this time. Please try again later.":
					self.response.out.write(response)
					return
				
			else:
				error = 'Please fill the Title and Content fields below!' 
			self.redirect('controlpanel.html')