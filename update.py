import logging
import string
import wsgiref.handlers
from google.appengine.api import users
from dbinterface import DataStoreInterface
from google.appengine.ext import webapp
from util.sessions import Session
from stringFormatter import StringFormatter
from datetime import datetime
import render

class UpdateHandler(webapp.RequestHandler):

    def get(self):
        datastore = DataStoreInterface()
        formatter = StringFormatter()
        
        path = self.request.query_string
        params =  path.split('/')
        company = params[0].replace('company=','')
        postId = params[1].replace('id=','')
        
        post = datastore.getPost(company, postId)
        
        for p in post:
            update = formatter.formatPost(p, company)
        
        render.doRender(self, 'update.html', {'update' : update})
        