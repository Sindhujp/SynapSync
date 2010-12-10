from dbinterface import DataStoreInterface
from google.appengine.ext import webapp
import render
from emailProcessor import EmailProcessor

class ContactHandler(webapp.RequestHandler):
    def get(self):
        render.doRender(self, 'contact.html', {'company':'synapsync'})
    
    def post(self):
        datastore = DataStoreInterface()  
        
        email = datastore.getAdminEmail('synapsync')      
        if (email <> 'null'):
            emailObj = EmailProcessor()
            subject = self.request.get('txtSubject')
            body = self.request.get('txtContent')
            
            emailObj.sendSupportEmail(email, subject, body) 
            render.doRender(self,'contact.html', {'confirmation' : 'Email sent!'})