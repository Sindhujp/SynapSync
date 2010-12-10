import string
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from util.sessions import Session
from dbinterface import DataStoreInterface
import render

class postActionHandler(webapp.RequestHandler):
    
    def get(self):
    
        self.session = Session()
        
        datastore = DataStoreInterface()
        query = self.request.query_string
        
        actionType = query.split('%')[0].split('&')[0].replace('action=','')
        postId = query.split('%')[0].split('&')[1].replace('id=','')
        
        if datastore.changePostStatus(postId, actionType) == 1:
            self.redirect('controlpanel.html')