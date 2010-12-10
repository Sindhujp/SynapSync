import logging
import string
import wsgiref.handlers
from google.appengine.ext.webapp \
    import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from dbinterface import DataStoreInterface
from google.appengine.ext import webapp
from util.sessions import Session
from dbinterface import DataStoreInterface
from stringFormatter import StringFormatter
from datastore import *
from django.http import *
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from urlparse import urlparse
from time import time
import render

# Import the Facebook helpers
import util.facebook.__init__ as facebook


API_KEY = 'bba630a5c803425bbb00cb137fe0894c'
SECRET_KEY = 'e55f6309bedf9a34a6334a5ccabf7bfe'



class FbAuthHandler(webapp.RequestHandler):
    
	def get(self):
	
		"""Get the user's friends and their pictures. This example uses
		   the Django web framework, but should be adaptable to others."""
	 
		# Get api_key and secret_key from a file
		fb = facebook.Facebook(API_KEY, SECRET_KEY)
	 
		# Present the login url
		return self.redirect(fb.get_login_url('http://crm.synapsync.com/facebook/callback/'))


class FbCallbackHandler(webapp.RequestHandler):

	def get(self):
	
		fb = facebook.Facebook(API_KEY, SECRET_KEY)
		url = urlparse(self.request.url)
		params = dict([part.split('=') for part in url[4].split('&')])
                
		userInfo = fb.__call__('Users.getInfo', {'session_key':params['fb_sig_session_key'], 'call_id':time(), 'uids':[params['fb_sig_user']], 'fields':['first_name', 'last_name']})
		
		render.doRender(self,'facebookcallback.html', {'currentUser':params['fb_sig_user'], 'token':params['auth_token'], 'firstn':userInfo[0]['first_name'], 'lastn':userInfo[0]['last_name']})

		
class FbSessionHandler(webapp.RequestHandler):

	def get(self):
	
		fb = facebook.Facebook(API_KEY, SECRET_KEY)
		url = self.request.url
		params = url.split('&')
		
		userID = params[0].split('?')[1]
		token = params[1].split('?')[1]
		fname = params[2].split('?')[1]
		lname = params[3].split('?')[1]
		
		newSessionKey = fb.__call__('Auth.getSession', {'auth_token':token})
		
		self.session = Session()
		formatter = StringFormatter()
		
		error = ''
		company = ''
        
		if 'user' not in self.session:
			error = 'Unauthorized User Error'
		else:
			user = self.session['user']
			company = formatter.getCompanyProfileName(user)
		
		if fb.__call__('Users.hasAppPermission', {'uid':userID, 'call_id':time(), 'ext_perm':'offline_access'}) == 0:
			error = 'Permissions Ungranted Error'
		
		if fb.__call__('Users.hasAppPermission', {'uid':userID, 'call_id':time(), 'ext_perm':'publish_stream'}) == 0:
			error = 'Permissions Ungranted Error'
		
		if fb.__call__('Users.hasAppPermission', {'uid':userID, 'call_id':time(), 'ext_perm':'read_stream'}) == 0:
			error = 'Permissions Ungranted Error'
		 
		query = db.Query(FbSession)
		query = query.filter('dbUid =', userID)
		results = query.fetch(limit = 1)
		
		if len(results) > 0:
			for r in results:
				if error == '':
					db.delete(r)
			
		if error == '':
			token = FbSession(dbProfileName = company, dbSessionKey = newSessionKey['session_key'], dbUserName = fname + ' ' + lname, dbUid = userID)
			token.put();
			self.response.out.write("Account added to SynapSync successfully! You may now return to the application.")
		else:
			self.response.out.write(error + ". Please try authenticating again.")