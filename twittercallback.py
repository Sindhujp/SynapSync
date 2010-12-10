import logging
import string
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import mail
from util.sessions import Session
from util.twitter_oauth_handler import *
from dbinterface import DataStoreInterface
from stringFormatter import StringFormatter
from datastore import *
import render

class TwitterCallbackHandler(webapp.RequestHandler):

    def get(self):

        self.session = Session()
        formatter = StringFormatter()
        client = OAuthClient('twitter', self, 'noName')
    
        token_info = client.getAccessToken(self.request.query_string.split('=')[1])
        error = ''
        company = ''
        
        if 'user' not in self.session:
            error = 'Unauthorized User Error'
        else:
            user = self.session['user']
            company = formatter.getCompanyProfileName(user)
        values = formatter.getValues(token_info)
        
        #Must use dbInterface
        query = db.Query(UserToken)
        query = query.filter('dbTwitterName=', values[3])
        results = query.fetch(limit = 1)
        
        if len(results) > 0:
            for r in results:
                db.delete(r)
                
        if error == '':
            token = UserToken(dbProfileName = company, dbTwitterName = values[3], dbToken = values[0], dbTokenSecret = values[1])
            token.put();
        self.redirect('settings.html')       		
        #render.doRender(self, 'settings.html', {'error' : error, 'message' : 'Twitter account ' + values[3] + ' added successfully!'})
        
